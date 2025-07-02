(define
	(problem mundobloques)
	(:domain mundobloques)
	(:objects
		A B C - bloque
	)
	(:init (sobre A C) (despejado A) (sobre-la-mesa B) (despejado B) (sobre-la-mesa C) (brazo-libre))
	(:goal (and (sobre-la-mesa A) (sobre B A) (sobre C B)))
)
