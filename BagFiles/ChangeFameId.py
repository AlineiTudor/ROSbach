import rosbag


bagin=rosbag.Bag("/home/alineitudor/Licenta/BagFiles/Circle.bag")
#print(bag)
times=[]
test=False
for a,b,c in bagin.read_messages(topics=['/BlueRov2/imu/data']):
    print(a)
    print("------")
    print(b)
    #print(type(b.header))
    print("------")
    print(type(c))
    print("------")
    print("/n/n/n")
    print(b.linear_acceleration.x)
    break
    for x in b.linear_acceleration_covariance:
        if x!=0:
            print(b)
            test=True
            break
    if test:
        break
    #print(a.timestamp)
#print(times)
'''
bagout=rosbag.Bag("/home/alineitudor/Licenta/BagFiles/Circle2.bag",'w')

for topic, msg, t in bagin:
    msg.header.frame_id="pixhawk"
    bagout.write(topic,msg,t)
bagout.close()
bagin.close()

bagout=rosbag.Bag("/home/alineitudor/Licenta/BagFiles/Circle2.bag")

for topic, msg, t in bagout:
    print(msg)
    break
bagout.close()'''





