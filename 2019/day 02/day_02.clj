; day_02.clj

(defn run 
    ([values] 
        (run values 0)
    )
    ([values start]    
        (let [op_code (get values start)]
            (cond 
                (< op_code 99)
                    (let [
                        a      (get values (get values (+ start 1)))
                        b      (get values (get values (+ start 2)))
                        output (get values (+ start 3))
                        ] 
                        (cond
                            (= op_code 1) (recur (assoc values output (+ a b)) (+ start 4))
                            (= op_code 2) (recur (assoc values output (* a b)) (+ start 4))
                            :else (assert false)
                        )
                    )
                        
                (= op_code 99) values
                :else (assert false)
            )
        )
    )
)

(assert (= (run [1,9,10,3,2,3,11,0,99,30,40,50]) [3500 9 10 70 2 3 11 0 99 30 40 50]))
(assert (= (run [1,0,0,0,99]) [2,0,0,0,99]))
(assert (= (run [2,3,0,3,99]) [2,3,0,6,99]))
(assert (= (run [2,4,4,5,99,0]) [2,4,4,5,99,9801]))
(assert (= (run [1,1,1,4,99,5,6,0,99]) [30,1,1,4,2,5,6,0,99]))

(defn toInt [x]
    (Integer/parseInt x)
)

(def data_txt (slurp "input.txt"))
(def data_splitted (clojure.string/split (clojure.string/trim-newline data_txt) #","))
(def data (vec (map toInt data_splitted)))

(defn set_noun_verb [data noun verb]
    (assoc (assoc data 1 noun) 2 verb)
)

(defn find_solution [data noun verb]
    (get (run (set_noun_verb data noun verb)) 0)
)

(println "Part 1:" (find_solution data 12 2))

; Part 2
(loop [noun 0 verb 0]    
    (if (= (find_solution data noun verb) 19690720)
        (println "Part 2:" (+ (* 100 noun) verb))
        (if (= noun 100)
            (recur 0 (inc verb))
            (recur (inc noun) verb)
        )
    )
)
