images-dir=./web
images=$(shell ls ${images-dir})
libs-dir=./lib
# Exclude setup.py as a lib
libs=$(shell ls ${libs-dir} | grep -v "setup.py")

build-images:
	$(foreach image, ${images}, $(MAKE) -C ${images-dir}/${image} build;)
push-images:
	$(foreach image, ${images}, $(MAKE) -C ${images-dir}/${image} push;)
build-libs:
	echo ${libs}
push-libs:
	$(foreach lib, ${libs}, /scripts/python/python-push.sh ${libs-dir}/${lib};)
