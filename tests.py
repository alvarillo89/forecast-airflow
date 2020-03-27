import api
import hug
import unittest
from falcon import HTTP_400, HTTP_200


class TestAPI(unittest.TestCase):

    def test_intervalo_incorrecto_v1(self):
        request = hug.test.get(api, "/servicio/v1/prediccion/badinterval")
        self.assertEqual(request.status, HTTP_400)
        self.assertEqual(request.data, 
            "Solo se admiten los siguientes intervalos: 24horas, 48horas y 72horas")
    
    def test_intervalo_incorrecto_v2(self):
        request = hug.test.get(api, "/servicio/v2/prediccion/badinterval")
        self.assertEqual(request.status, HTTP_400)
        self.assertEqual(request.data, 
            "Solo se admiten los siguientes intervalos: 24horas, 48horas y 72horas")

    def test_24horas_v1(self):
        request = hug.test.get(api, "/servicio/v1/prediccion/24horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 24)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())
    
    def test_48horas_v1(self):
        request = hug.test.get(api, "/servicio/v1/prediccion/48horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 48)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())
    
    def test_72horas_v1(self):
        request = hug.test.get(api, "/servicio/v1/prediccion/72horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 72)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())

    def test_24horas_v2(self):
        request = hug.test.get(api, "/servicio/v2/prediccion/24horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 24)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())
    
    def test_48horas_v2(self):
        request = hug.test.get(api, "/servicio/v2/prediccion/48horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 48)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())
    
    def test_72horas_v2(self):
        request = hug.test.get(api, "/servicio/v2/prediccion/72horas")
        self.assertEqual(request.status, HTTP_200)
        self.assertTrue(len(request.data) == 72)
        self.assertTrue("hour" in request.data[0].keys())
        self.assertTrue("temp" in request.data[0].keys())
        self.assertTrue("hum" in request.data[0].keys())


if __name__ == "__main__":
    unittest.main(verbosity=2) 