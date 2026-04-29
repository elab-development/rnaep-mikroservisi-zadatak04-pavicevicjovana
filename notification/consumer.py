from database import redis

GROUP = 'notification-group'
CONSUMER = 'notification-consumer'
STREAMS = ['order_completed', 'refund_order']

for stream in STREAMS:
    try:
        redis.xgroup_create(stream, GROUP, mkstream=True)
    except:
        print(f'Group {GROUP} on {stream} already exists!')

while True:
    try:
        results = redis.xreadgroup(
            GROUP, CONSUMER,
            {stream: '>' for stream in STREAMS},
            count=1, block=5000
        )
        if results:
            for result in results:
                stream_name = result[0]
                messages = result[1]
                for msg_id, data in messages:
                    order_id = data.get('pk', 'N/A')
                    if stream_name == 'order_completed':
                        print(f"Obaveštenje: Porudžbina {order_id} je uspešno kreirana i plaćena")
                    elif stream_name == 'refund_order':
                        print(f"Obaveštenje: Porudžbina {order_id} je refundirana")
                    redis.xack(stream_name, GROUP, msg_id)
    except Exception as e:
        print(f"Consumer error: {e}")
