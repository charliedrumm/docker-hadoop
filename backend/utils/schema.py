import graphene
from graphene import List, String, Int

class SymptomAnalysis(graphene.ObjectType):
    disease = String()
    symptoms = List(String)
    outcome = String()
    count = Int()