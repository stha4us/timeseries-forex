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
forex_forecast:
	python api/model/timeseries/run_ingest.py
	python api/model/timeseries/run_train.py 
	python api/model/timeseries/run_model_predict.py
	python api/model/timeseries/run_report.py
