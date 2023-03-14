.PHONY: build
build:
	docker build . -t forex


.PHONY: run
run:
	docker run --env-file .env -it -v "$$(pwd):/forex" forex bash

.PHONY: run-jupyter
run-jupyter:
	docker run --env-file .env -it -p 8888:8000 -v "$$(pwd):/forex" forex sh -c "pip install jupyter && jupyter notebook --allow-root --no-browser --ip=0.0.0.0"


.PHONY: run_pipeline
run_pipeline:
	python forex/scripts/run_config.py
	python forex/scripts/run_staging.py
	python forex/scripts/run_train.py
	python forex/scripts/run_forecast.py
	python forex/scripts/run_postprocess.py