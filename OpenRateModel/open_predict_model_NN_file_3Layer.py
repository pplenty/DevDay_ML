import tensorflow as tf
import numpy as np

# kohyusik
# data file : target.txt (rows=117600)
xy = np.loadtxt('target.txt', unpack=True, dtype='float32', delimiter=',')
x_data = np.transpose(xy[1:-1]) # N x 4 Maxrix
y_data = np.reshape(xy[-1], (len(x_data), 1)) # N x 1 Maxrix
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

# input data level tune
mat_modul = tf.constant([[4.,0.,0.,0.], [0.,1.,0.,0.], [0.,0.,0.5,0.], [0.,0.,0.,25.]])
modulation = tf.matmul(x_data, mat_modul)

sess2 = tf.Session()
sess2.run(mat_modul)
x_data = sess2.run(modulation)

print 'x  : \n' , x_data
print 'y  : \n' , y_data


X = tf.placeholder(tf.float32, name='x-input')
Y = tf.placeholder(tf.float32, name='y-output')


w1 = tf.Variable(tf.random_uniform([4, 5], -0.5, 0.5), name='weight1')
w2 = tf.Variable(tf.random_uniform([5, 10], -0.5, 0.5), name='weight2')
w3 = tf.Variable(tf.random_uniform([10, 10], -0.5, 0.5), name='weight3')
w4 = tf.Variable(tf.random_uniform([10, 1], -0.5, 0.5), name='weight4')


b1 = tf.Variable(tf.zeros([5]), name="Bias1")
b3 = tf.Variable(tf.zeros([10]), name="Bias3")
b2 = tf.Variable(tf.zeros([10]), name="Bias2")
b4 = tf.Variable(tf.zeros([1]), name="Bias4")


L2 = tf.nn.relu(tf.matmul(X, w1) + b1)
L3 = tf.nn.relu(tf.matmul(L2, w2) + b2)
L4 = tf.nn.relu(tf.matmul(L3, w3) + b3)


# hypothesis
hypothesis = tf.sigmoid(tf.matmul(L4, w4) + b4)
#h = tf.matmul(L8, w8) + b8
#hypothesis = tf.div(1., 1.+tf.exp(-h))

# cost function
with tf.name_scope('cost') as scope:
    cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))

with tf.name_scope('train') as scope:
    a = tf.Variable(0.1)
    optimizer = tf.train.GradientDescentOptimizer(a)
    train = optimizer.minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)

    for step in xrange(20001):
        sess.run(train, feed_dict={X: x_data, Y: y_data})
        if step % 200 == 0:
            print step, sess.run(cost, feed_dict={X: x_data, Y: y_data}), sess.run(w1), sess.run(w2)

    correct_prediction = tf.equal(tf.floor(hypothesis + 0.5), Y)

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print sess.run([hypothesis, tf.floor(hypothesis + 0.5), correct_prediction], feed_dict={X: x_data, Y: y_data})
    print "accuracy", accuracy.eval({X: x_data, Y: y_data})

    print "TEST INPUT : \n"
    print sess.run(hypothesis, feed_dict={X: [[12, 13, 50/2, 0*25]]}) > 0.5
    print sess.run(hypothesis, feed_dict={X: [[20, 10, 25, 0]]}) > 0.5
    # print sess.run(hypothesis, feed_dict={X:[[20., 15., 5., 1.], [20., 15., 5., 1.]] })  # > 0.5
    # print sess.run(hypothesis, feed_dict={X:[[20, 15, 5, 1]] })[0][0]  # > 0.5




    # file write
    f = open('test.csv', 'w')
    f.write("w1 : \n" + str(sess.run(w1)) + "\n")
    f.write("w2 : \n" + str(sess.run(w2)) + "\n")
    f.write("w3 : \n" + str(sess.run(w3)) + "\n")
    f.write("w4 : \n" + str(sess.run(w4)) + "\n")

    f.write("b1 : \n" + str(sess.run(b1)) + "\n")
    f.write("b2 : \n" + str(sess.run(b2)) + "\n")
    f.write("b3 : \n" + str(sess.run(b3)) + "\n")
    f.write("b4 : \n" + str(sess.run(b4)) + "\n")



    f.write("\n\n#######################\n\n")
    for w_day in xrange(7):
        day = w_day * 4
        for w_time in xrange(24):
            time = w_time
            for w_ages in xrange(8):
                ages = (w_ages + 1) * 5
                for w_gender in xrange(1):
                    gender = w_gender * 25.
                    w_result = sess.run(hypothesis, feed_dict={X: [[day, time, ages, gender]]})[0][0]

                    f.write(str(w_day) + "," + str(w_time) + "," + str(ages * 2) + "," + str(w_gender) + "," + str(round(w_result, 4) * 100))
                    f.write("\n")

    f.close()

