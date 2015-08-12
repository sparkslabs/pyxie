
all:
	@echo "iterators - Make 'traditional' exception oriented iterators"
	@echo "transform - Make the transformed version that's non macro based first, etc"
	@echo "noexceptions - Make the no-exceptions version using new macros"

iterators:
	g++ -Wall iterators.cpp -o iterators

transform:
	g++ -Wall iterators_transform.cpp -o transform

noexceptions:
	g++ -Wall iterators_noexceptions.cpp -o noexceptions

clean:
	rm -f iterators
	rm -f transform
	rm -f noexceptions
	rm -f *~
