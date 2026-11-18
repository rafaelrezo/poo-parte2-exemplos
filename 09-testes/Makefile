CXX ?= g++
PYTHON ?= python3
CXXFLAGS := -std=c++17 -Wall -Wextra -Werror -pedantic
PYTHONPATH := $(CURDIR)/src
export PYTHONPATH

.PHONY: test test-cpp test-python clean

test: test-cpp test-python

test-cpp: build/teste_medicao
	./build/teste_medicao

test-python: build/produtor_fixture
	$(PYTHON) -m unittest discover -s tests/python -p 'test_*.py' -v

build/teste_medicao: tests/cpp/teste_medicao.cpp src/cpp/medicao.hpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) -Isrc/cpp tests/cpp/teste_medicao.cpp -o $@

build/produtor_fixture: src/cpp/produtor_fixture.cpp
	mkdir -p build
	$(CXX) $(CXXFLAGS) src/cpp/produtor_fixture.cpp -o $@

clean:
	rm -rf build
