class TextDataset(Dataset):

    def __init__(self, file_path):
        self.file_path = file_path

    def __getitem__(self):
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        enc = tiktoken.encoding_for_model("gpt-4")
        encoded_data = enc.encode(text)
        
        return encoded_data


enc = tiktoken.encoding_for_model("gpt-4")
num_vocab = enc.n_vocab
print(num_vocab)

clean_text = TextDataset('test/test.txt')
clean_data = clean_text.__getitem__()

corruptor = TextCorruptor('test/test.txt', mistake_probability=0.1)
corruptor.corrupt_text()
corruptor.save_corrupted_text('corrupted_test_output.txt')

noisy_text = TextDataset('corrupted_test_output.txt')
noisy_data = noisy_text.__getitem__()
def create_batches(clean_text, noisy_text, block_size):
    # Generate input sequences from noisy text
    noisy_inputs = torch.stack([torch.tensor(noisy_text[i:i+block_size]) for i in range(len(noisy_text)-block_size+1)])

    print("Noisy inputs are ready!")
    
    # Generate corresponding target sequences from clean text
    clean_targets = torch.stack([torch.tensor(clean_text[i+1:i+block_size+1]) for i in range(len(clean_text)-block_size)])

    print("Clean inputs are ready!")
    
    return noisy_inputs.to(device), clean_targets.to(device)

# Example usage:

block_size = 100
noisy_inputs, clean_targets = create_batches(clean_data, noisy_data, block_size)