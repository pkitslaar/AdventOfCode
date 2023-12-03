const EXAMPLE_DATA: &str = indoc::indoc! {"
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"};

const EXAMPLE_DATA2: &str = indoc::indoc! {"
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"};

extern crate regex;
use regex::Regex;

fn solve(data: &str, part2: bool) -> Option<String> {
    let mut sum = 0;

    let mut word_values = std::collections::HashMap::new();
    word_values.insert(r"\d", "");
    if part2 {
        word_values.insert("one", "1");
        word_values.insert("two", "2");
        word_values.insert("three", "3");
        word_values.insert("four", "4");
        word_values.insert("five", "5");
        word_values.insert("six", "6");
        word_values.insert("seven", "7");
        word_values.insert("eight", "8");
        word_values.insert("nine", "9");
        word_values.insert("zero", "0");
    }

    // Combine all keys in WORD_VALUES into a single regex
    let word_re = Regex::new(
        word_values
            .keys()
            .cloned()
            .collect::<Vec<&str>>()
            .join("|")
            .as_str(),
    )
    .unwrap();

    for line in data.lines() {
        let mut digits = Vec::new();
        let mut start = 0;
        loop {
            if let Some(mat) = word_re.find(&line[start..]) {
                let match_str = mat.as_str();
                let match_value = word_values.get(match_str).unwrap_or(&match_str);
                digits.push(*match_value);
                start += mat.start() + match_str.len();
                if match_str.len() > 1 {
                    start -= 1
                }
            } else {
                break;
            }
        }
        let combined = format!("{}{}", digits.first()?, digits.last()?);
        sum += combined.parse::<u32>().ok()?;
    }
    Some(sum.to_string())
}

fn example() {
    let result = solve(EXAMPLE_DATA, false).unwrap();
    println!("example: {}", result);
    assert_eq!(result, "142");
}

#[test]
fn test_example() {
    example()
}

fn part1() {
    let data = data();
    let result = solve(data, false).unwrap();
    println!("Part 1: {}", result);
    assert_eq!(result, "55017");
}

#[test]
fn test_part1() {
    part1()
}

fn example2() {
    let result = solve(EXAMPLE_DATA2, true).unwrap();
    println!("example2: {}", result);
    assert_eq!(result, "281");
}

#[test]
fn test_example2() {
    example2()
}

fn part2() {
    let data = data();
    let result = solve(data, true).unwrap();
    println!("Part 2: {}", result);
    assert_eq!(result, "53539");
}

#[test]
fn test_part2() {
    part2()
}

fn data() -> &'static str {
    let data = include_str!("./input.txt");
    data
}

fn main() {
    example();
    part1();
    example2();
    part2();
}
