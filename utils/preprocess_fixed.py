import tensorflow as tf

IMG_SIZE = (224,224)
BATCH_SIZE = 32

def load_data(train_path, test_path):
    
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        train_path,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int'
    )

    test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        test_path,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int'
    )

    train_dataset = train_dataset.map(lambda x,y:(x/255.0,y))
    test_dataset = test_dataset.map(lambda x,y:(x/255.0,y))

    return train_dataset, test_dataset
