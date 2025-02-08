import unittest
from app.services.resume_parser import parse_resume

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.sample_resume_text = """
        John Doe
        john.doe@example.com
        +1234567890
        Experience: Software Engineer at Google
        Skills: Python, Machine Learning, Docker
        """

    def test_parse_name(self):
        parsed_data = parse_resume(self.sample_resume_text)
        self.assertEqual(parsed_data["name"], "John Doe")

    def test_parse_email(self):
        parsed_data = parse_resume(self.sample_resume_text)
        self.assertEqual(parsed_data["email"], "john.doe@example.com")

    def test_parse_phone(self):
        parsed_data = parse_resume(self.sample_resume_text)
        self.assertEqual(parsed_data["phone"], "+1234567890")

    def test_parse_skills(self):
        parsed_data = parse_resume(self.sample_resume_text)
        self.assertIn("Python", parsed_data["skills"])
        self.assertIn("Machine Learning", parsed_data["skills"])
        self.assertIn("Docker", parsed_data["skills"])

    def test_parse_job_role(self):
        parsed_data = parse_resume(self.sample_resume_text)
        self.assertEqual(parsed_data["job_role"], "Software Engineer")

if __name__ == '__main__':
    unittest.main()
