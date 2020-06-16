from starlette.applications import Starlette
from starlette.routing import Route
from starlette.graphql import GraphQLApp
import graphene
import ctypes
import uvicorn


class Count:
	main = 0


class Date(graphene.ObjectType):
	month = graphene.Int()
	day = graphene.Int()
	year = graphene.Int()


class User(graphene.ObjectType):
	first_name = graphene.String()
	last_name = graphene.String()
	birthday = graphene.Field(Date)
	age = graphene.Int()
	user_id = graphene.String()

	@staticmethod
	def resolve_first_name(parent, info):
		return "Elijah"

	@staticmethod
	def resolve_last_name(parent, info):
		return "Cobb"

	@staticmethod
	def resolve_birthday(parent, info):
		return Date(month=6, day=3, year=1999)

	@staticmethod
	def resolve_age(parent, info):
		return 21


class Velocity(graphene.ObjectType):
	x = graphene.Float()
	y = graphene.Float()
	z = graphene.Float()


class SubSystem(graphene.ObjectType):
	temp = graphene.Float()
	velocity = graphene.Field(Velocity)
	name = graphene.String()

	@staticmethod
	def resolve_velocity(parent, info):
		return Velocity(x=1.2, y=2.3, z=10.1)


class Math(graphene.ObjectType):
	cube = graphene.Int(num=graphene.Int())
	pow = graphene.Int(num=graphene.Int(), exp=graphene.Int())

	@staticmethod
	def resolve_cube(parent, info, num):
		return ctypes.CDLL("./test.so").myCube(num)

	@staticmethod
	def resolve_pow(parent, info, num, exp):
		return ctypes.CDLL("./test.so").myPow(num, exp)


class Queries(graphene.ObjectType):

	count = graphene.Int(description="A global count that is incremented from 'increment' mutation.")
	user = graphene.Field(User, user_id=graphene.String())
	math = graphene.Field(Math)
	subsystem = graphene.Field(SubSystem, args={
		"name": graphene.String()
	})

	@staticmethod
	def resolve_count(parent, info):
		return Count.main

	@staticmethod
	def resolve_user(parent, info, user_id):
		return User(user_id=user_id)

	@staticmethod
	def resolve_math(parent, info):
		return Math()

	@staticmethod
	def resolve_subsystem(parent, info, name):
		return SubSystem(temp=32.1, name=name)


class MutateCount(graphene.Mutation):

	class Arguments:
		value = graphene.Int()

	count = graphene.Int()

	@staticmethod
	def resolve_count(parent, info):
		return Count.main

	@staticmethod
	def mutate(parent, info, value):
		pass


class AddCount(MutateCount):
	@staticmethod
	def mutate(parent, info, value):
		Count.main += value
		return AddCount.Field()


class MultiplyCount(MutateCount):
	@staticmethod
	def mutate(parent, info, value):
		Count.main *= value
		return MultiplyCount.Field()


class Mutations(graphene.ObjectType):
	add = AddCount.Field()
	multiply = MultiplyCount.Field()


uvicorn.run(Starlette(routes=[
	Route("/", GraphQLApp(schema=graphene.Schema(query=Queries, mutation=Mutations)))
]))
