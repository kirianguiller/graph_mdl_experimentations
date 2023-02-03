source /root/projects/DeSDA/venv/bin/activate


# 3. Preparing input for SQS
python "/root/projects/DeSDA/Chapter 3 - MDL/Tools/sqs_input_file_maker_conllu.py"  /data/tatoebaAligned/es-fr_small/es.conllu /data/tatoebaAligned/es-fr_small/
python "/root/projects/DeSDA/Chapter 3 - MDL/Tools/sqs_input_file_maker_conllu.py"  /data/tatoebaAligned/es-fr_small/fr.conllu /data/tatoebaAligned/es-fr_small/

# 4. Running SQS
/root/tools/sqs-main -i /data/tatoebaAligned/es-fr_small/es.conllu.dat -o /data/tatoebaAligned/es-fr_small/es.res -m search
/root/tools/sqs-main -i /data/tatoebaAligned/es-fr_small/es.conllu.dat -o /data/tatoebaAligned/es-fr_small/es.ord -m order -p /data/tatoebaAligned/es-fr_small/es.res

/root/tools/sqs-main -i /data/tatoebaAligned/es-fr_small/fr.conllu.dat -o /data/tatoebaAligned/es-fr_small/fr.res -m search
/root/tools/sqs-main -i /data/tatoebaAligned/es-fr_small/fr.conllu.dat -o /data/tatoebaAligned/es-fr_small/fr.ord -m order -p /data/tatoebaAligned/es-fr_small/fr.res

# 5. Interpreting SQS's output
python "/root/projects/DeSDA/Chapter 3 - MDL/Tools/sqs_output_interpreter.py" /data/tatoebaAligned/es-fr_small/es.ord /data/tatoebaAligned/es-fr_small/es.conllu.lab
python "/root/projects/DeSDA/Chapter 3 - MDL/Tools/sqs_output_interpreter.py" /data/tatoebaAligned/es-fr_small/fr.ord /data/tatoebaAligned/es-fr_small/fr.conllu.lab

# 7. Detecting syntactic differences automatically using the Minimum Description Length principle
python "/root/projects/DeSDA/Chapter 3 - MDL/Tools/MDL_difference_detector.py"