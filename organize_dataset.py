import os
import shutil
import random

def organize_dataset():
    """Organize dataset into proper class folders"""
    
    # Define class folders
    classes = ['normal', 'benign', 'malignant']
    
    # Create organized directories
    for split in ['train', 'test']:
        for class_name in classes:
            os.makedirs(f'dataset/{split}/{class_name}', exist_ok=True)
    
    # Get all image files
    train_files = []
    test_files = []
    
    # Collect files from train/train
    train_dir = 'dataset/train/train'
    if os.path.exists(train_dir):
        for file in os.listdir(train_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                train_files.append(os.path.join(train_dir, file))
    
    # Collect files from test/test
    test_dir = 'dataset/test/test'
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_files.append(os.path.join(test_dir, file))
    
    print(f"Found {len(train_files)} training files")
    print(f"Found {len(test_files)} testing files")
    
    # Distribute files evenly among classes (for demo purposes)
    # In a real dataset, files should already be labeled by class
    
    def distribute_files(files, split):
        # Simple distribution: assign files to classes based on filename patterns
        # This is just for demonstration - real datasets should have proper labels
        
        for i, file_path in enumerate(files):
            filename = os.path.basename(file_path)
            
            # Simple heuristic based on filename (adjust based on your actual naming)
            if 'normal' in filename.lower():
                class_name = 'normal'
            elif 'benign' in filename.lower():
                class_name = 'benign'
            elif 'malignant' in filename.lower():
                class_name = 'malignant'
            else:
                # Random assignment for demonstration
                class_name = classes[i % len(classes)]
            
            # Copy to appropriate folder
            dest_path = f'dataset/{split}/{class_name}/{filename}'
            shutil.copy2(file_path, dest_path)
            print(f"Moved {filename} to {class_name}")
    
    # Distribute files
    distribute_files(train_files, 'train')
    distribute_files(test_files, 'test')
    
    print("Dataset organization completed!")

if __name__ == "__main__":
    organize_dataset()
