; Day 1 puzzle - Advent of Code 2019
; Pieter Kitslaar

(defn fuel_for_mass [mass]
  (- (int (/ mass 3.0)) 2)
)

(assert (== (fuel_for_mass 12) 2))
(assert (== (fuel_for_mass 14) 2))
(assert (== (fuel_for_mass 1969) 654))
(assert (== (fuel_for_mass 100756) 33583))

(defn toInt [x]
  (Integer/parseInt x)
)

(def modules_masses (map toInt (clojure.string/split-lines (slurp "input.txt"))))

; Part 1
(println "Part 1" (apply + (map fuel_for_mass modules_masses)))

; Part 2
(defn recursive_fuel [mass]
  (loop [current_mass mass total 0]
    (let [new_fuel (fuel_for_mass current_mass)]
      (if (<= new_fuel 0)
        total
        (recur new_fuel (+ new_fuel total))
      )
    )
  )
)

(assert (== (recursive_fuel 12) 2))
(assert (== (recursive_fuel 1969) 966))
(assert (== (recursive_fuel 100756) 50346))

(println "Part 2" (apply + (map recursive_fuel modules_masses)))
