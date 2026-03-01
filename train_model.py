import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers, models, optimizers, callbacks
import os
import json
from datetime import datetime

# Configuration
TRAIN_PATH = "dataset/train/train"
TEST_PATH = "dataset/test/test"
MODEL_SAVE_PATH = "models/densenet121_model.h5"
HISTORY_SAVE_PATH = "models/training_history.json"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10  # Reduced for demo

def load_data(train_path, test_path):
    """Load and preprocess data"""
    
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

def create_model():
    """Create and compile the DenseNet-121 model"""
    
    # Load DenseNet-121 base model
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    
    # Freeze the base model initially
    base_model.trainable = False
    
    # Add custom classification layers
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(3, activation='softmax')(x)
    
    # Create the complete model
    model = models.Model(inputs=base_model.input, outputs=output)
    
    # Compile the model
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model, base_model

def train_model():
    """Main training function"""
    
    print("Starting Breast Cancer Detection Model Training...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load and prepare data
    print("Loading and preprocessing data...")
    train_dataset, test_dataset = load_data(TRAIN_PATH, TEST_PATH)
    
    # Get class names
    class_names = ['normal', 'benign', 'malignant']
    print(f"Class names: {class_names}")
    
    # Create the model
    print("Creating DenseNet-121 model...")
    model, base_model = create_model()
    
    # Define callbacks
    callbacks_list = [
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            filepath=MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train the model
    print("\n=== Training ===")
    history = model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=EPOCHS,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Evaluate the model
    print("\n=== Model Evaluation ===")
    test_loss, test_accuracy = model.evaluate(test_dataset, verbose=1)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Save the final model
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved to {MODEL_SAVE_PATH}")
    
    # Save training history
    combined_history = {
        'history': {key: [float(x) for x in values] for key, values in history.history.items()},
        'final_metrics': {
            'test_accuracy': float(test_accuracy),
            'test_loss': float(test_loss)
        },
        'class_names': class_names,
        'training_date': datetime.now().isoformat()
    }
    
    with open(HISTORY_SAVE_PATH, 'w') as f:
        json.dump(combined_history, f, indent=2)
    
    print(f"Training history saved to {HISTORY_SAVE_PATH}")
    print("\n=== Training Complete! ===")
    
    return model, combined_history

if __name__ == "__main__":
    # Check if dataset exists
    if not os.path.exists(TRAIN_PATH) or not os.path.exists(TEST_PATH):
        print(f"Error: Dataset not found at {TRAIN_PATH} or {TEST_PATH}")
        exit(1)
    
    # Start training
    try:
        model, history = train_model()
        print("Training completed successfully!")
    except Exception as e:
        print(f"Training failed with error: {str(e)}")
        exit(1)
