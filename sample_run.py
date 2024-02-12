import os
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset, load_from_disk, Audio

dataset_root = os.getenv("DATASETDIR")

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny", low_cpu_mem_usage=True)
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model.to("cuda")

try:
    # datasetにはreazonspeechを想定
    dataset = load_from_disk(dataset_root)
    text_key = 'transcription'
except:
    dataset = load_dataset('mozilla-foundation/common_voice_13_0', "ja", split="validation", streaming=True)
    dataset = dataset.cast_column("audio", Audio(sampling_rate=processor.feature_extractor.sampling_rate))
    text_key = 'sentence'

data = next(iter(dataset))
inputs = processor(data["audio"]["array"], sampling_rate=16000, return_tensors="pt")
input_features = inputs.input_features

#forced_decoder_ids = processor.tokenizer.get_decoder_prompt_ids(language='ja', task='transcribe')
# generate_kwargs = {
#     'forced_decoder_ids': forced_decoder_ids,
# }

try:
    generated_ids = model.generate(
        input_features.to("cuda"),
        #generate_kwargs=generate_kwargs, # generate_kwargsが指定できるのは4.21.0など古いバージンのみ
        task='transcribe',
        language='ja',
        max_new_tokens=128)
    pred_text = processor.decode(generated_ids[0], skip_special_tokens=True)

    print("Ground Truth:", data[text_key])
    print("Pred text:", pred_text)
    print('Preparing envrionment is done.')
except BaseException as e:
    print(f'Failed with {e}')