import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers, models, optimizers, callbacks
from utils.preprocess import load_data
import os
import json
from datetime import datetime

# Configuration
TRAIN_PATH = "dataset/train"
TEST_PATH = "dataset/test"
MODEL_SAVE_PATH = "models/densenet121_model.h5"
HISTORY_SAVE_PATH = "models/training_history.json"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30

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
        metrics=['accuracy', 'Precision', 'Recall']
    )
    
    return model, base_model

def fine_tune_model(model, base_model):
    """Fine-tune the model by unfreezing some layers"""
    
    # Unfreeze the top layers of the base model
    base_model.trainable = True
    
    # Freeze all layers except the last 50
    for layer in base_model.layers[:-50]:
        layer.trainable = False
    
    # Recompile with a lower learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', 'Precision', 'Recall']
    )
    
    return model

def train_model():
    """Main training function"""
    
    print("Starting Breast Cancer Detection Model Training...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load and prepare data
    print("Loading and preprocessing data...")
    train_dataset, test_dataset = load_data(TRAIN_PATH, TEST_PATH)
    
    # Get class names from the dataset
    class_names = train_dataset.class_names
    print(f"Class names: {class_names}")
    
    # Create the model
    print("Creating DenseNet-121 model...")
    model, base_model = create_model()
    
    # Print model summary
    print("\nModel Architecture:")
    model.summary()
    
    # Define callbacks
    callbacks_list = [
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            filepath=MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        callbacks.TensorBoard(
            log_dir='logs/fit/' + datetime.now().strftime('%Y%m%d-%H%M%S'),
            histogram_freq=1
        )
    ]
    
    # Phase 1: Initial training with frozen base
    print("\n=== Phase 1: Initial Training ===")
    history_phase1 = model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=EPOCHS // 2,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Phase 2: Fine-tuning
    print("\n=== Phase 2: Fine-Tuning ===")
    model = fine_tune_model(model, base_model)
    
    history_phase2 = model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=EPOCHS // 2,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Evaluate the model
    print("\n=== Model Evaluation ===")
    test_loss, test_accuracy, test_precision, test_recall = model.evaluate(test_dataset, verbose=1)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Precision: {test_precision:.4f}")
    print(f"Test Recall: {test_recall:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Save the final model
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved to {MODEL_SAVE_PATH}")
    
    # Save training history
    combined_history = {
        'phase1': {key: [float(x) for x in values] for key, values in history_phase1.history.items()},
        'phase2': {key: [float(x) for x in values] for key, values in history_phase2.history.items()},
        'final_metrics': {
            'test_accuracy': float(test_accuracy),
            'test_precision': float(test_precision),
            'test_recall': float(test_recall),
            'test_loss': float(test_loss)
        },
        'class_names': class_names,
        'training_date': datetime.now().isoformat()
    }
    
    with open(HISTORY_SAVE_PATH, 'w') as f:
        json.dump(combined_history, f, indent=2)
    
    print(f"Training history saved to {HISTORY_SAVE_PATH}")
    
    # Generate classification report
    print("\n=== Classification Report ===")
    y_true = []
    y_pred = []
    
    for images, labels in test_dataset:
        predictions = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(tf.argmax(predictions, axis=1).numpy())
    
    # Print confusion matrix
    from sklearn.metrics import confusion_matrix, classification_report
    import numpy as np
    
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    print("\n=== Training Complete! ===")
    print(f"Model ready for use at: {MODEL_SAVE_PATH}")
    
    return model, combined_history

if __name__ == "__main__":
    # Check if dataset exists
    if not os.path.exists(TRAIN_PATH) or not os.path.exists(TEST_PATH):
        print(f"Error: Dataset not found at {TRAIN_PATH} or {TEST_PATH}")
        print("Please ensure the dataset is properly organized in the dataset/ directory")
        exit(1)
    
    # Start training
    try:
        model, history = train_model()
        print("Training completed successfully!")
    except Exception as e:
        print(f"Training failed with error: {str(e)}")
        exit(1)
