import tensorflow as tf
import numpy as np
x_data= np.array([[0,0],[0,1],[1,0],[1,1]],dtype=np.float32)
y_data=np.array([[0],[1],[1],[0]],dtype=np.float32)
X=tf.placeholder(tf.float32)
Y=tf.placeholder(tf.float32)


with tf.name_scope("layer1") as scope:
    with tf.name_scope("layer1"):
        W1 = tf.Variable(tf.random_normal([2, 2]), name='weight1')
    b1 = tf.Variable(tf.random_normal([2]), name='bias1')
    layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

layer1_hist = tf.summary.histogram("layer1", layer1)


with tf.name_scope("layer2") as scope:
    with tf.name_scope("layer2"):
        W2 = tf.Variable(tf.random_normal([2, 1]), name='weight2')
    b2 = tf.Variable(tf.random_normal([1]), name='bias2')
    hypothesis = tf.sigmoid(tf.matmul(layer1, W2) + b2)





hypothesis_hist = tf.summary.histogram("hypothesis", hypothesis)

with tf.name_scope("cost") as scope:

    with tf.name_scope("cost"):
        cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) *
                               tf.log(1 - hypothesis))
    cost_summ = tf.summary.scalar("cost", cost)
with tf.name_scope("train") as scope:
    with tf.name_scope("train"):
        train = tf.train.AdamOptimizer(learning_rate=0.1).minimize(cost)

    # Accuracy computation
    # True if hypothesis>0.5 else False
predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))
accuracy_summ = tf.summary.scalar("accuracy", accuracy)

# Launch graph
with tf.Session() as sess:
    # tensorboard --logdir=./logs/xor_logs
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("C:\\Users\\조유선\\PycharmProjects\\untitled\\logs")
    writer.add_graph(sess.graph)  # Show the graph

    # Initialize TensorFlow variables
    sess.run(tf.global_variables_initializer())

    for step in range(10001):
        summary, _ = sess.run([merged_summary, train], feed_dict={X: x_data, Y: y_data})
        writer.add_summary(summary, global_step=step)

        if step % 100 == 0:
            print(step, sess.run(cost, feed_dict={
                X: x_data, Y: y_data}), sess.run([W1, W2]))

    # Accuracy report
    h, c, a = sess.run([hypothesis, predicted, accuracy],
                       feed_dict={X: x_data, Y: y_data})
    print("\nHypothesis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)