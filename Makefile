#!make
include .env
export

run:
	unicorn main:app --reload

