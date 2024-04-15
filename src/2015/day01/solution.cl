; I mean come on, the problem is *literally* called "Not Quite Lisp"

(defun get-chars (filename)
    "Reads in the given filename char by char"
    (declare (string filename))
    (with-open-file (stream filename)
        (loop for char_out = (read-char stream nil)
        while char_out
        collect char_out
        )
    )
)

(defun paren-to-int (char_in)
    "( maps to 1, ) maps to -1"
    (declare (character char_in))
    (cond 
        ((string-equal char_in "(")  1) ; ( -> 1
        ((string-equal char_in ")") -1) ; ) -> -1
        (t                       0)     ; else 0
    ) 
)

(defun find-crossover (input_seq)
    "Walks through the sequence until we find the basement"
    (declare (list input_seq))
    (loop 
        ; Variable declaration
        for x in input_seq
        for i from 1

        ; Do this every loop
        sum x into total ; implicitely starts at 0

        ; Exit condition
        when (eq total -1) return i
    )
)

(let ((int_in (mapcar #'paren-to-int (get-chars "input.txt"))))
    (format T "Part 1: ~d~%"
        (apply '+ int_in)
    )
    (format T "Part 2: ~d"
        (find-crossover int_in)
    )
    (terpri)
)


