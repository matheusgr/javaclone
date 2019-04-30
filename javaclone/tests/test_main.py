import unittest


import main


class TestMain(unittest.TestCase):
    def test_java_code(self):
        code =   """public class Code {
                        private int test = 0;
                    }"""
        print(main.process_java_code(code))
        self.assertEqual(1, 1)

    def test_java_code_complex(self):
        code =   """public class Code {
                        private int test = 0;
                        private String s;
                        private Code(String s) {
                            this.s = s;
                        }
                        private int value() {
                            return this.test;
                        }
                    }"""
        print(main.process_java_code(code))
        self.assertEqual(1, 1)


    def test_invalid_java_code(self):
        code =   b"""public class Code {
                        private int test = 0;
                        private String s;
                        private Code(String s) {
                            this.s = s;
                        }
                        private int value() {
                            return this.test;
                        }
                    """
        print(main.process_content(code))
        self.assertEqual(1, 1)

