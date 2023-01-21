import tensorflow as tf

def checkGPU():
    device_name = tf.test.gpu_device_name()
    if not device_name:
        raise SystemError('GPU device not found')
        exit()
    
    print('Found GPU at: {}'.format(device_name))