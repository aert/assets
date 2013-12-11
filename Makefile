
PROJECT_NAME=assets
PROJECT_VERSION:=$(shell python version.py)
PROJECT_FILENAME=$(PROJECT_NAME)_$(PROJECT_VERSION)
VAGRANT_PATH=deploy

CONF=`pwd`/assets/etc/config_develop.ini
FIXTURES=deploy/ansible/roles/app_assets/files

PIP_CACHE=./build/pip_cache

##  Installation Paths:
#PREFIX?=/usr


## default target, it's what to do if you typed "make" without target
default: 
	@echo "-- default target: empty"
	
	
## This target englob all the targets on this makefile
all:  clean develop vagrant_setup


## clean temporary files after a building operation
clean:
	@echo "Cleaning..." 
	@rm -rf public/assets/
	@rm -rf `find . -name *.pyc`
	@rm -rf `find . -name *.pyo`
	@rm -rf docs/build

clean_all:
	@$(MAKE) clean
	@rm -rf build


# DEVELOP
# #######

develop:
	@pip install -e .[testing] --download-cache $(PIP_CACHE)

develop_init: develop_deps develop

develop_deps:
	@sudo apt-get install python-dev
	# For wheel
	@pip install --upgrade pip setuptools
	@mkdir -p logs

runserver:
	export APP_CONFIG_ASSETS=$(CONF); aert-assets runserver 0.0.0.0:8002

validate:
	export APP_CONFIG_ASSETS=$(CONF); cd assets; ./manage.py validate

syncdb:
	export APP_CONFIG_ASSETS=$(CONF); aert-assets syncdb --noinput
	export APP_CONFIG_ASSETS=$(CONF); aert-assets loaddata $(FIXTURES)/initial_data_auth.yaml
	export APP_CONFIG_ASSETS=$(CONF); aert-assets loaddata $(FIXTURES)/initial_data_students.yaml
	export APP_CONFIG_ASSETS=$(CONF); aert-assets loaddata $(FIXTURES)/initial_data_earnings.yaml
	export APP_CONFIG_ASSETS=$(CONF); aert-assets loaddata $(FIXTURES)/initial_data_spendings.yaml
	export APP_CONFIG_ASSETS=$(CONF); aert-assets loaddata $(FIXTURES)/initial_data_invoices.yaml

raven_test:
	export APP_CONFIG_ASSETS=$(CONF); aert-assets raven test

messages:
	export APP_CONFIG_ASSETS=$(CONF); cd assets; ./manage.py makemessages -a

messages_compile:
	export APP_CONFIG_ASSETS=$(CONF); cd assets; ./manage.py compilemessages

semantic_latest:
	@mkdir -p build/
	@rm -rf build/semantic*
	cd build; wget http://semantic-ui.com/build/semantic.zip; unzip semantic.zip -d semantic
	@rm -rf assets/common/static/vendor/semantic/
	mv build/semantic/packaged assets/common/static/vendor/semantic/
	@rm -rf build/semantic*

# VAGRANT
# #######

vagrant: installer vagrant_up 

vagrant_halt:
	@cd $(VAGRANT_PATH); vagrant halt

vagrant_up:
	@cd $(VAGRANT_PATH); vagrant up

vagrant_ssh:
	@cd $(VAGRANT_PATH); vagrant up; vagrant ssh

vagrant_reload:
	@cd $(VAGRANT_PATH); vagrant reload

vagrant_destroy:
	@cd $(VAGRANT_PATH); vagrant destroy

vagrant_provision: installer vagrant_reprovision

vagrant_reprovision: 
	@cd $(VAGRANT_PATH); vagrant provision

# DEPLOYMENT
# ##########

tag:
	@while [ -z "$$NEW_TAG" ]; do \
			read -r -p "New tag: " NEW_TAG; \
	done; \
	git tag -a $$NEW_TAG -m "Created tag: $$NEW_TAG"; \
	git push --tags;

installer: develop installer_clean wheel installer_archive

installer_clean:
	@rm -rf dist
	@mkdir -p build/installer
	@rm -rf build/setup_*

wheel:
	@pip wheel --wheel-dir=build/wheel/wheel-dir . --download-cache $(PIP_CACHE)
	@mv build/wheel/wheel-dir build/installer/wheel-dir
	@rm -rf build/wheel/

installer_archive:
	@cp deploy/installer/Makefile build/installer/
	@sed -i 's/__VERSION__/$(PROJECT_VERSION)/g' build/installer/Makefile
	@cp deploy/installer/requirements.txt build/installer/
	@mv build/installer/ build/setup_$(PROJECT_FILENAME)
	@cd build; tar -czf setup_$(PROJECT_FILENAME).tgz setup_$(PROJECT_FILENAME)/

