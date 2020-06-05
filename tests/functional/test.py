import unittest
import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_register(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/register")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("username").send_keys("gihan")
        driver.find_element_by_id("firstName").send_keys("gihan")
        driver.find_element_by_id("lastName").send_keys("ravindu")
        driver.find_element_by_id("email").send_keys("gihan@test.com")
        driver.find_element_by_id("password").send_keys("testing")
        driver.find_element_by_id("confirmPassword").send_keys("testing")
        time.sleep(2)
        driver.find_element_by_id("register_btn").click()
        actualUrl = "http://phylogenetic-tree.herokuapp.com/"
        time.sleep(10)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_existing_register(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/register")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("username").send_keys("gihan")
        driver.find_element_by_id("firstName").send_keys("gihan")
        driver.find_element_by_id("lastName").send_keys("ravindu")
        driver.find_element_by_id("email").send_keys("gihan@test.com")
        driver.find_element_by_id("password").send_keys("testing")
        driver.find_element_by_id("confirmPassword").send_keys("testing")
        time.sleep(2)
        driver.find_element_by_id("register_btn").click()
        actualUrl = "http://phylogenetic-tree.herokuapp.com/register"
        time.sleep(10)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
    
    def test_false_register(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/register")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("username").send_keys("gihan")
        driver.find_element_by_id("firstName").send_keys("gihan")
        driver.find_element_by_id("lastName").send_keys("ravindu")
        driver.find_element_by_id("email").send_keys("gihan@test.com")
        driver.find_element_by_id("password").send_keys("testing")
        driver.find_element_by_id("confirmPassword").send_keys("wrong")
        time.sleep(2)
        driver.find_element_by_id("register_btn").click()
        actualUrl = "http://phylogenetic-tree.herokuapp.com/register"
        time.sleep(10)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_login(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/login")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("username").send_keys("gihan")
        driver.find_element_by_id("password").send_keys("testing")
        time.sleep(2)
        driver.find_element_by_id("login_btn").click()
        actualUrl = "http://phylogenetic-tree.herokuapp.com/"
        time.sleep(10)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
    
    def test_login(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/login")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("username").send_keys("gihan")
        driver.find_element_by_id("password").send_keys("restapi")
        time.sleep(2)
        driver.find_element_by_id("login_btn").click()
        actualUrl = "http://phylogenetic-tree.herokuapp.com/login"
        time.sleep(10)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_generate_phylogenetic_tree(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/login")
        driver.find_element_by_id("username").send_keys("rest")
        driver.find_element_by_id("password").send_keys("restapi")
        time.sleep(2)
        driver.find_element_by_id("login_btn").click()
        time.sleep(5)
        driver.get("http://phylogenetic-tree.herokuapp.com/matrix/67")
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("start_btn").click()
        time.sleep(5)
        actualUrl="http://phylogenetic-tree.herokuapp.com/tree"
        expectedUrl= driver.current_url
        self.assertTrue(actualUrl in expectedUrl)

    def test_update_phylogenetic_tree(self):
        driver = self.driver
        driver.get("http://phylogenetic-tree.herokuapp.com/login")
        driver.find_element_by_id("username").send_keys("rest")
        driver.find_element_by_id("password").send_keys("restapi")
        time.sleep(2)
        driver.find_element_by_id("login_btn").click()
        time.sleep(5)
        driver.get("http://phylogenetic-tree.herokuapp.com/tree/41")
        time.sleep(5)
        self.assertIn("Phylogentic Tree Visualizer", driver.title)
        driver.find_element_by_id("add_specie").click()
        time.sleep(3)
        driver.find_element_by_id("specie_0").click()
        driver.find_element_by_id("update_btn").click()
        time.sleep(60)
        actualUrl = "http://phylogenetic-tree.herokuapp.com/tree/41"
        expectedUrl = driver.current_url
        self.assertEqual(expectedUrl,actualUrl)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()