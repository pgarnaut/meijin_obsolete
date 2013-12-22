# Makefile for OSX/Linux

SUPPRESSED_WARNINGS=-Wno-unused-function -Wno-unused-variable -Wno-unused-value
CFLAGS=-g -Wall $(SUPPRESSED_WARNINGS) -I.
CXXFLAGS=$(CFLAGS)
LDFLAGS=-g

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	CCFLAGS += -DLINUX
	CXX=g++
	CC=gcc
	CFLAGS +=
	CXXFLAGS += -std=gnu++0x 
	LDFLAGS += -lrt
endif
ifeq ($(UNAME_S),Darwin)
	CXX=clang++
	CC=clang
	CFLAGS +=
	CXXFLAGS += -std=c++11 -stdlib=libc++ 
	LDFLAGS += -stdlib=libc++ -framework Security -framework Foundation
endif


PROJECT = meijin

OBJECTS = main.o \
		board.o


DEFINES = -DLINUX

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(DEFINES) $<
	
.c.o:
	$(CC) -c $(CFLAGS) $(DEFINES) $<
	
$(PROJECT): $(OBJECTS)
	$(CXX) -o $(PROJECT) *.o $(LDFLAGS) 


clean:
	rm -f *.lo *.o *.a