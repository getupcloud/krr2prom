IMAGE_TAG    := prometheus-workload-loader
IMAGE_REPO   := getupcloud/krr2prom
IMAGE_NAME   := $(IMAGE_REPO):$(IMAGE_TAG)
IMAGE_LATEST := $(IMAGE_REPO):latest
KRR_GIT_REF  ?= $(IMAGE_TAG)

build:
	docker build . -t $(IMAGE_NAME) --build-arg KRR_GIT_REF=$(KRR_GIT_REF)

tag:
	git tag $(IMAGE_TAG)

release: build tag
	docker push $(IMAGE_NAME)
	docker push $(IMAGE_LATEST)
	git push --tags
