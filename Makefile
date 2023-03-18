.PHONY: build
build:
	docker build . -t timeseries_forex

.PHONY: run
run:
	docker run --env-file .env -it -v "$$(pwd):/home/ec2-user/TIMESERIES_FOREX" timeseries_forex bash

.PHONY: run-jupyter
run-jupyter:
	docker run --env-file .env -it -p 8888:8888 -v "$$(pwd):/home/ec2-user/TIMESERIES_FOREX" timeseries_forex  sh -c "pip install jupyter && jupyter notebook --allow-root --no-browser --ip=0.0.0.0"

.PHONY: build-and-run
build-and-run: build run

.PHONY: clean
clean: docker system prune

.PHONY: asp_forecast
asp_forecast:
	python api/timeseries/run_ingest.py
	python api/timeseries/run_train.py 
	python api/timeseries/run_model_predict.py
	python api/timeseries/run_report.py

.PHONY: run_pipeline
run_pipeline:
	python forex/scripts/run_config.py
	python forex/scripts/run_staging.py
	python forex/scripts/run_train.py
	python forex/scripts/run_forecast.py
	python forex/scripts/run_postprocess.py