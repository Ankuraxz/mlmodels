""""

Related to data procesisng



"""






def torchvision_dataset_MNIST_load(path, **args):
    from torchvision import datasets, transforms
    train_dataset = datasets.MNIST(path, train=True, download=True,
                    transform=transforms.Compose([
                        transforms.Grayscale(num_output_channels=3),
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                    ]))
    valid_dataset = datasets.MNIST(path, train=False,
                    transform=transforms.Compose([
                        transforms.Grayscale(num_output_channels=3),
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                    ]))
    return train_dataset, valid_dataset  




def wrap_torch_datasets(sets, args_list = None, **args):
    if not isinstance(sets,list) and not isinstance(sets,tuple):
        sets = [sets]
    import torch
    if args_list is None:
        return [torch.utils.data.DataLoader(x,**args) for x in sets]
    return [torch.utils.data.DataLoader(x,**a,**args) for a,x in zip(args_list,sets)]







def torch_transform_mnist():
    from torchvision import datasets, transforms
    transform=transforms.Compose([
                        transforms.Grayscale(num_output_channels=3),
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
    ])
    return transform





def load_function(package="mlmodels.util", name="path_norm"):
  import importlib
  return  getattr(importlib.import_module(package), name)




def get_dataset_torch(data_pars):
    """"
     MNIST Fashion-MNIST KMNIST EMNIST QMNIST  FakeData COCO Captions Detection LSUN ImageFolder DatasetFolder 
     ImageNet CIFAR STL10 SVHN PhotoTour SBU Flickr VOC Cityscapes SBD USPS Kinetics-400 HMDB51 UCF101 CelebA

     Sentiment Analysis
    SST
    IMDb
    Question Classification
    TREC
    Entailment
    SNLI
    MultiNLI
    Language Modeling
    WikiText-2
    WikiText103
    PennTreebank
    Machine Translation
    Multi30k
    IWSLT
    WMT14
    Sequence Tagging
    UDPOS
    CoNLL2000Chunking
    Question Answering
    BABI20

    """




    if  data_pars["transform"]  :
       transform = load_function(  data_pars.get("preprocess_module", "mlmodels.preprocess.image"), 
                                   data_pars.get("transform", "torch_transform_mnist" ))
    else :
       transform = None


    if data_pars['train_path'] :
      pass


    if data_pars['test_path'] :
      pass




    
    dataset_module =  data_pars.get('dataset_module', "torchvision.datasets")   
    dset = load_function(dataset_module), data_pars["dataset"]

    train_loader = torch.utils.data.DataLoader( dset(data_pars['data_path'], train=True, download=True, transform= transform),
                                                batch_size=data_pars['train_batch_size'], shuffle=True)
    
    valid_loader = torch.utils.data.DataLoader( dset(data_pars['data_path'], train=False, download=True, transform= transform),
                                                batch_size=data_pars['train_batch_size'], shuffle=True)

    return train_loader, valid_loader  














def tf_dataset(dataset_pars):
    """
        Save in numpy compressez format TF Datasets
    
        dataset_pars ={ "dataset_id" : "mnist", "batch_size" : 5000, "n_train": 500, "n_test": 500, 
                            "out_path" : "dataset/vision/mnist2/" }
        tf_dataset(dataset_pars)
        
        
        https://www.tensorflow.org/datasets/api_docs/python/tfds
        import tensorflow_datasets as tfds
        import tensorflow as tf
        
        # Here we assume Eager mode is enabled (TF2), but tfds also works in Graph mode.
        print(tfds.list_builders())
        
        # Construct a tf.data.Dataset
        ds_train = tfds.load(name="mnist", split="train", shuffle_files=True)
        
        # Build your input pipeline
        ds_train = ds_train.shuffle(1000).batch(128).prefetch(10)
        for features in ds_train.take(1):
          image, label = features["image"], features["label"]
          
          
        NumPy Usage with tfds.as_numpy
        train_ds = tfds.load("mnist", split="train")
        train_ds = train_ds.shuffle(1024).batch(128).repeat(5).prefetch(10)
        
        for example in tfds.as_numpy(train_ds):
          numpy_images, numpy_labels = example["image"], example["label"]
        You can also use tfds.as_numpy in conjunction with batch_size=-1 to get the full dataset in NumPy arrays from the returned tf.Tensor object:
        
        train_ds = tfds.load("mnist", split=tfds.Split.TRAIN, batch_size=-1)
        numpy_ds = tfds.as_numpy(train_ds)
        numpy_images, numpy_labels = numpy_ds["image"], numpy_ds["label"]
        
        
        FeaturesDict({
    'identity_attack': tf.float32,
    'insult': tf.float32,
    'obscene': tf.float32,
    'severe_toxicity': tf.float32,
    'sexual_explicit': tf.float32,
    'text': Text(shape=(), dtype=tf.string),
    'threat': tf.float32,
    'toxicity': tf.float32,
})
            
            
    
    """
    import tensorflow_datasets as tfds

    d          = dataset_pars
    dataset_id = d['dataset_id']
    batch_size = d.get('batch_size', -1)  # -1 neans all the dataset
    n_train    = d.get("n_train", 500)
    n_test     = d.get("n_test", 500)
    out_path   = path_norm(d['out_path'] )
    name       = dataset_id.replace(".","-")    
    os.makedirs(out_path, exist_ok=True) 


    train_ds =  tfds.as_numpy( tfds.load(dataset_id, split= f"train[0:{n_train}]", batch_size=batch_size) )
    test_ds  = tfds.as_numpy( tfds.load(dataset_id, split= f"test[0:{n_test}]", batch_size=batch_size) )
    # val_ds  = tfds.as_numpy( tfds.load(dataset_id, split= f"test[0:{n_test}]", batch_size=batch_size) )

    print("train", train_ds.shape )
    print("test",  test_ds.shape )

    def get_keys(x):
       if "image" in x.keys() : xkey = "image"
       if "text" in x.keys() : xkey = "text"    
       return xkey
    
    
    for x in train_ds:
       #print(x)
       xkey =  get_keys(x)
       np.savez_compressed(out_path + f"{name}_train" , X = x[xkey] , y = x.get('label') )
        

    for x in test_ds:
       #print(x)
       np.savez_compressed(out_path + f"{name}_test", X = x[xkey] , y = x.get('label') )
        
    print(out_path, os.listdir( out_path ))
        
      










