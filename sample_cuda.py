import torch

# Check if CUDA is available
cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")

# If CUDA is available, get more details
if cuda_available:
    print(f"Number of GPUs available: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}") # Prints name of the first GPU
    
    # Check memory usage (optional)
    print("Memory Usage:")
    print(f"Allocated: {round(torch.cuda.memory_allocated(0)/1024**3,1)} GB")
    print(f"Cached: {round(torch.cuda.memory_reserved(0)/1024**3,1)} GB")
    
    # Create a tensor and move it to GPU
    x = torch.randn(3, 3).cuda()
    print(f"Tensor on GPU: {x.is_cuda}")
else:
    print("CUDA is not available on this system. PyTorch will use CPU.")
