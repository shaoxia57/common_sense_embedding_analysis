export TRAIN_FILE=../data/finetune_data/sample_from_sets/train_sentences.txt
export TEST_FILE=../data/finetune_data/sample_from_sets/eval_sentences.txt

CUDA_VISIBLE_DEVICES=7 python ../transformers/examples/run_language_modeling.py \
    --output_dir=../models/gpt-2/sample_from_set/ \
    --model_type=gpt2 \
    --per_gpu_train_batch_size=1 \
    --per_gpu_eval_batch_size=1 \
    --model_name_or_path=gpt2 \
    --do_train \
    --train_data_file=$TRAIN_FILE \
    --do_eval \
    --eval_data_file=$TEST_FILE
