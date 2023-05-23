import argparse

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def get_args():
    parser = argparse.ArgumentParser()
    # experimental results
    parser.add_argument('--dataset_folder', type=str, default='/home/data')
    parser.add_argument('--splits', action=ListAction, default=['train', 'val', 'test'], 
            help='splitting of the dataset')
    args = parser.parse_args()
    return args
