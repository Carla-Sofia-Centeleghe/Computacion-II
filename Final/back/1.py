# Para revisar la versión de cuDNN, se puede utilizar el siguiente codigo:

import tensorflow as tf
print(tf.sysconfig.get_build_info()['cudnn_version'])


