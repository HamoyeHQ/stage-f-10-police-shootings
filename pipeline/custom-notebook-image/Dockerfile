FROM gcr.io/kubeflow-images-public/tensorflow-2.1.0-notebook-cpu:1.0.0

USER root

RUN pip3 install pandas \
		google-cloud-storage \
		kubeflow-metadata \
		kfp --upgrade --user

ENV NB_PREFIX /
