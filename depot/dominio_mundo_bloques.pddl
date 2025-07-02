(define
	(domain mundobloques)
	(:requirements :strips :typing)
	(:types
		bloque - object
	)
	(:predicates
		(agarrado ?b - bloque)
		(brazo-libre )
		(despejado ?b - bloque)
		(sobre ?b1 - bloque ?b2 - bloque)
		(sobre-la-mesa ?b - bloque)
	)
	(:action agarrar
		:parameters (?b - bloque)
		:precondition (and (sobre-la-mesa ?b) (despejado ?b) (brazo-libre ))
		:effect (and (agarrado ?b) (not (sobre-la-mesa ?b)) (not (despejado ?b)) (not (brazo-libre )))
	)
	(:action apilar
		:parameters (?b1 - bloque ?b2 - bloque)
		:precondition (and (agarrado ?b1) (despejado ?b2))
		:effect (and (sobre ?b1 ?b2) (despejado ?b1) (brazo-libre ) (not (agarrado ?b1)) (not (despejado ?b2)))
	)
	(:action bajar
		:parameters (?b - bloque)
		:precondition (agarrado ?b)
		:effect (and (sobre-la-mesa ?b) (despejado ?b) (brazo-libre ) (not (agarrado ?b)))
	)
	(:action desapilar
		:parameters (?b1 - bloque ?b2 - bloque)
		:precondition (and (sobre ?b1 ?b2) (despejado ?b1) (brazo-libre ))
		:effect (and (agarrado ?b1) (despejado ?b2) (not (sobre ?b1 ?b2)) (not (despejado ?b1)) (not (brazo-libre )))
	)
)