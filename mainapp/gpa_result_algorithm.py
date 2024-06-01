def get_total_units(courses):
    total_units = sum(course["units"] for course in courses)
    return total_units


def possible_scores(course_info, desired_gpa):
  def calculate_total_units():
    return sum(course["units"] for course in course_info)

  def calculate_max_score():
    return sum(5 * course["units"] for course in course_info)

  def calculate_gpa(scores):
    total_score = sum(score * course["units"] for score, course in zip(scores, course_info))
    return total_score / calculate_max_score() * 5

  def is_feasible(scores):
    return calculate_gpa(scores) >= desired_gpa and 0 not in scores

  def backtrack(scores, course_idx, valid_count, valid_scores):
    if course_idx == len(course_info) or valid_count >= 100:
      if is_feasible(scores):
        valid_scores.append(scores.copy())
        return valid_count + 1
      return valid_count

    possible_grades = [5, 4, 3, 2, 0] if course_info[course_idx]["units"] > 0 else [5, 4, 3, 2]
    possible_grades.reverse()

    max_possible_gpa = calculate_gpa(scores[:course_idx] + [5] * (len(course_info) - course_idx))
    if max_possible_gpa < desired_gpa:
      return valid_count

    for grade in possible_grades:
      scores[course_idx] = grade
      valid_count = backtrack(scores, course_idx + 1, valid_count, valid_scores)
      if valid_count >= 100:
        break

    return valid_count

  scores = [0] * len(course_info)
  valid_scores = []
  backtrack(scores, 0, 0, valid_scores)

  formatted_output = []
  for idx, scores in enumerate(valid_scores):
    formatted_courses = []
    for course, score in zip(course_info, scores):
      formatted_courses.append({"code": course["code"], "name": course["name"], "units": course["units"], "possible_grade": score})
    formatted_output.append(formatted_courses)

  return formatted_output[:100]  # Return only the first 100 valid combinations


def generate_possible_results(gpa, courses):
    results = []

    possible_scores_list = possible_scores(courses, float(gpa))
    for idx, scores in enumerate(possible_scores_list):
        results.append(scores)

    return results


# Example usage
if __name__ == '__main__':
    course_info = [
        {"code": "BIO111", "name": "BIOLOGY", "units": 3},
        {"code": "CHM111", "name": "CHEMISTRY", "units": 3},
        {"code": "CHM119", "name": "CHEM PRAC", "units": 1},
        {"code": "CIT111", "name": "MS OFFICE", "units": 0},
        {"code": "CSC111", "name": "COMP SCI", "units": 3},
        {"code": "CST111", "name": "LIBRARY", "units": 2},
        {"code": "EDS111", "name": "ENTREPRENUER", "units": 1},
        {"code": "GST111", "name": "ENGLISH", "units": 2},
        {"code": "MAT111", "name": "ALGEBRA", "units": 3},
        {"code": "MATH112", "name": "TRIG", "units": 2},
        {"code": "PHY111", "name": "PHYSICS", "units": 2},
        {"code": "PHY119", "name": "PHY PRAC", "units": 1},
        {"code": "TMC111", "name": "TOTAL MAN", "units": 1},
        {"code": "TMC112", "name": "JOGGING", "units": 0}
    ]

    desired_gpa = 3.5

    generate_possible_results(desired_gpa, course_info)

    # possible_scores_list = possible_scores(course_info, desired_gpa)
    # for idx, scores in enumerate(possible_scores_list):
    #     print(f"Combination {idx + 1}: {scores}")
