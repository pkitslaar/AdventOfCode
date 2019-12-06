(require '[taoensso.tufte :as tufte :refer (defnp p profiled profile)])

;; We'll request to send `profile` stats to `println`:
(tufte/add-basic-println-handler! {})

(def UNIT_MOVES {
    "R" [ 1  0]
    "L" [-1  0]
    "U" [ 0  1]
    "D" [ 0 -1]
})

(defn sum_pos
    [a b]
    (p :sum_pos
        [(+ (first a) (first b)) (+ (second a) (second b))])
)

(defn code_to_move [code]
    (p :code_to_move
    (let [[c & d] code]
        (let [  move (get UNIT_MOVES (str c))
                num_steps (Integer/parseInt (apply str d))
            ]
            (repeat num_steps move)
        )
    ))
)

(code_to_move "R47")


(defn wire_to_moves 
    [wire]
    (p :wire_to_moves
    (apply concat (map code_to_move (clojure.string/split wire #",")))))

(wire_to_moves "R5,D2")

(defn moves_to_positions
    [moves inital_pos]
    (p :moves_to_positions
    (reduce (fn [pos mov]
            (into pos [(sum_pos (last pos) mov)]))
            [inital_pos]
            moves)))

(defn wire_to_positions
    [wire]
    (moves_to_positions (wire_to_moves wire) [0,0]))

(wire_to_positions "R5,D2")

(defn find_cross_points
    [wire1 wire2]
    (let [wire1_path (wire_to_positions wire1)
          wire2_path (wire_to_positions wire2)
          cross_points (p :set_intersect (clojure.set/intersection (set wire1_path) (set wire2_path)))]
            [(disj cross_points [0,0]) wire1_path wire2_path]))

(find_cross_points "R3,U2" "U2,R3")

(defn abs [v] (java.lang.Math/abs v))

(defn manhattan [point]
    (p :manhattan
    (reduce + (map abs point)))
)

(defn closest_cross
    [wire1 wire2]
    (let [cross_points (first (find_cross_points wire1 wire2))
          sorted_points (p :sort_by (sort-by manhattan cross_points))
         ]
            (manhattan (first sorted_points))
        )
)

(closest_cross "R3,U2" "U2,R3")

(assert (= (closest_cross "R8,U5,L5,D3" "U7,R6,D4,L4") 6))
(assert (= (closest_cross "R75,D30,R83,U83,L12,D49,R71,U7,L72" "U62,R66,U55,R34,D71,R55,D58,R83") 159))
(assert (= (closest_cross "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51" "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") 135))

(def wires (clojure.string/split-lines (slurp "input.txt")))

(first wires)
(second wires)



(profile ; Profile any `p` forms called during body execution
    {} ; Profiling options; we'll use the defaults for now
    (find_cross_points (first wires) (second wires)))
