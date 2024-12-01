// Day 1 of Advent of Code 2024
// Never used Rust before, and this is usually the easiest day,
// so there's no time like the present to give it a test drive

use clap::{Arg, Command};
use std::fs::File;
use std::path::Path;
use std::io::{BufReader, BufRead};

/// Parse the command line arguments
/// 
/// # Returns
///     
/// The command line arguments
fn parse_args() -> clap::ArgMatches {
    let parser = Command::new("Advent of Code 2024 Day 01")
        .version("1.0.0")
        .author("James Dean")
        .about("Solution for https://adventofcode.com/2024/day/1")
        .arg(Arg::new("filename")
            .required(true)
            .help("The input file to use")
            .index(1));
    parser.get_matches()
}

/// Read the input file
/// 
/// # Arguments
/// 
/// * `path` - Path object pointed at the input file
/// 
/// # Returns
/// 
/// A tuple containing two I32 vectors, consistnign of
/// column 1 and column 2 from the input file
fn read_input(path: &Path) -> (Vec<i32>, Vec<i32>) {
    // Open up the file
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);

    // These are small vectors, so I'm okay with resize overhead
    // in favor for readability
    let mut vec1 = Vec::new();
    let mut vec2 = Vec::new();

    // Read the file into our vectors
    for line in reader.lines() {
        let line = line.expect("Failed to read line");
        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|str| str.parse::<i32>().expect("Failed to parse number"))
            .collect(); // collect() converts iterator --> vector
        vec1.push(nums[0]);
        vec2.push(nums[1]);
    }
    
    // Sort and return 'em
    vec1.sort();
    vec2.sort();

    (vec1, vec2)
}

/// Problem 1 - Manhattan Distance
/// 
/// # Arguments
/// 
/// * `vec1` - Borrow of the first vector
/// * `vec2` - Borrow of the second vector
/// 
/// # Returns
/// 
/// The Manhattan distance between the two vectors
fn problem1(vec1: &[i32], vec2: &[i32]) -> i32 {
    let mut distance = 0;
    for (num1, num2) in vec1.iter().zip(vec2.iter()) {
        distance += (num1 - num2).abs();
    }
    distance
}

/// Problem 2 - Similarity Sum
/// 
/// # Arguments
/// 
/// * `vec1` - Borrow of the first vector
/// * `vec2` - Borrow of the second vector
/// 
/// # Returns
/// 
/// The sum of the numbers that are the same in both vectors
fn problem2(vec1: &[i32], vec2: &[i32]) -> i32 {
    let mut similarity = 0;
    for num1 in vec1.iter() {
        for num2 in vec2.iter() {
            if num1 == num2 {
                similarity += num1;
            }
            // The vectors are sorted, so we can stop early
            if num2 > num1 {
                break;
            }
        }
    }
    similarity
}

fn main() {
    // Read the inputs
    let args = parse_args();
    let path = Path::new(args.value_of("filename").unwrap());
    let (vec1, vec2) = read_input(path);

    // Solve the problems
    let solution1 = problem1(&vec1, &vec2);
    let solution2 = problem2(&vec1, &vec2);

    // Print the results
    println!("Solution 1: {}", solution1);
    println!("Solution 2: {}", solution2);
}
