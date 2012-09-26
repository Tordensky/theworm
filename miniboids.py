import pygame
import math
import time
import random
from pygame.locals import*
pygame.init()

screen_res = (250, 250)

screen = pygame.display.set_mode((screen_res), 0, 32)

class Vector2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __repr__(self):
		return "Vector(%s, %s)" % (self.x, self.y)
		
	def __add__(self, b):
		return Vector2D(self.x + b.x, self.y + b.y)
	
	def __sub__(self, b):
		return Vector2D(self.x - b.x, self.y - b.y)
	
	def __mul__(self, b):
		if type(b) == type(1.0):
			return Vector2D(self.x * b, self.y * b)
		raise "Can't do that yet"
	
	def __div__ (self, b):
		return Vector2D(self.x / b.x, self.y / b.y)
	
	def __abs__(self):
		return (abs(self.x), abs(self.y))
	
	def magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def normalized(self):
		m = self.magnitude()
		return Vector2D(self.x / m, self.y / m)
	
	def copy(self):
		return Vector2D(self.x, self.y)


class Boid(Vector2D):
	def __init__(self):
		Vector2D.__init__(self, 0, 0)
		# Movement
		self.pos = Vector2D((screen.get_width()*random.random()), (screen.get_height()*random.random()))
		self.speed = Vector2D(100, 100)
		self.average_heading_flock = Vector2D(0, 0)
		self.avoid_collison_flock_member = Vector2D(0, 0)
		self.avoid_collison_object = Vector2D(0,0)
		self.avoid_collison_hoik = Vector2D(0,0)
		self.center_flock = Vector2D(0, 0)
		self.max_speed = 140.0
		self.min_speed = 70.0
		self.turn_speed = 12.8
		
		# Radius
		self.flock_radius = 70
		self.hoik_escape_radius = 75
		self.collision_radius = 15
		self.collision_radius_objects = 20
		self.collision_radius_other_boids = 25
		
		# Graphics
		self.radius = 4
		self.color = (0, 0, 255)
		self.color_in_flock = (255,255,255)
		self.color_not_in_flock = (0,0,255)
		self.tail_length = 10
		self.tail_stroke = 3
		
		# Status
		self.in_flock = False
		self.ignore_flock = False
	
	def update_vectors(self, boids, hoiks, objects):
		self.center_flock = Vector2D(0, 0)
		self.average_heading_flock = Vector2D(0, 0)
		self.avoid_collison_flock_member = Vector2D(0, 0)
		flock_members = 0
		collision_members = 0
		for other_boid in boids:
			if self.pos != other_boid.pos:
				dp1p2 = self.pos - other_boid.pos
				# Check for flock members
				if self.flock_radius + other_boid.radius >= dp1p2.magnitude():
					# Ignore flock if chased by hoik
					if not self.ignore_flock:
						self.center_flock = self.center_flock + other_boid.pos
					
					# Calculate average heading flock
					self.average_heading_flock = self.average_heading_flock + other_boid.speed
					flock_members += 1
					
					# Check for collision other boids
					if self.collision_radius_other_boids + other_boid.radius >= dp1p2.magnitude():
						collision_members += 1
						self.avoid_collison_flock_member = self.avoid_collison_flock_member + other_boid.pos
		
		# Flock behavior
		if flock_members != 0:
			self.in_flock = True
			# Ignore flock if chased by hoik
			if not self.ignore_flock:
				# Average center for flock
				self.center_flock.x = (self.center_flock.x / flock_members)
				self.center_flock.y = (self.center_flock.y / flock_members)
				self.center_flock.x = ((self.center_flock.x - self.pos.x)/40)
				self.center_flock.y = ((self.center_flock.y - self.pos.y)/40)
			
			# Average heading for flock
			self.average_heading_flock.x = (self.average_heading_flock.x / flock_members)
			self.average_heading_flock.y = (self.average_heading_flock.y / flock_members)
			self.average_heading_flock.x = ((self.average_heading_flock.x - self.speed.x)/40)
			self.average_heading_flock.y = ((self.average_heading_flock.y - self.speed.y)/40)
		else:
			self.in_flock = False
			
		# Flock collision
		if collision_members != 0:
			# Preventing collision course with other flock members
			self.avoid_collison_flock_member.x = (self.avoid_collison_flock_member.x / collision_members)
			self.avoid_collison_flock_member.y = (self.avoid_collison_flock_member.y / collision_members)
			self.avoid_collison_flock_member.x = (self.pos.x - self.avoid_collison_flock_member.x)
			self.avoid_collison_flock_member.y = (self.pos.y - self.avoid_collison_flock_member.y)
		
		# Calculate color for boid.(If not in flock turn to color_not_in_flock)
		if self.in_flock:
			self.color = self.color_in_flock
		elif not self.in_flock:
			self.color = self.color_not_in_flock
			
		# Esacape Hoik hunting this boid
		self.avoid_collison_hoik = Vector2D(0,0)
		hunting_me_members = 0
		
		for hoik in hoiks:
			dp1p2 = self.pos - hoik.pos
			if self.hoik_escape_radius + hoik.radius >= dp1p2.magnitude():
				self.ignore_flock = True
				hunting_me_members += 1
				self.avoid_collison_hoik = self.avoid_collison_hoik + hoik.pos
				
		# Hoiks Hunting me
		if hunting_me_members != 0:
			# Preventing collision course with other flock members
			self.avoid_collison_hoik.x = (self.avoid_collison_hoik.x / hunting_me_members)
			self.avoid_collison_hoik.y = (self.avoid_collison_hoik.y / hunting_me_members)
			self.avoid_collison_hoik.x = (self.pos.x - self.avoid_collison_hoik.x)
			self.avoid_collison_hoik.y = (self.pos.y - self.avoid_collison_hoik.y)
			
		else:
			self.ignore_flock = False

		# Object collision
		self.avoid_collison_object = Vector2D(0, 0)
		for object in objects:
			# Preventing object collision
			dp1p2 = self.pos - object.pos
			if self.collision_radius_objects + object.radius >= dp1p2.magnitude():
				self.avoid_collison_object.x = object.pos.x
				self.avoid_collison_object.y = object.pos.y
				self.avoid_collison_object.x = (self.pos.x - self.avoid_collison_object.x)/2
				self.avoid_collison_object.y = (self.pos.y - self.avoid_collison_object.y)/2
				# Actual collision
				if self.radius + object.radius >= dp1p2.magnitude():
			 		self.speed = dp1p2

					

	def move(self, time_passed_seconds):
		# Calculate new speed vector
		self.speed = self.speed + self.center_flock + self.average_heading_flock + self.avoid_collison_flock_member + self.avoid_collison_object + self.avoid_collison_hoik
		
		# If Boids moves to slow speed them up
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) < self.min_speed:
			self.speed = self.speed * 1.3 
		
		# If Boids moves to fast slow them down
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) > self.max_speed:
			self.speed = self.speed * 0.9 
		
		distx = time_passed_seconds * self.speed.x
		disty = time_passed_seconds * self.speed.y
		self.pos.x = self.pos.x + distx
		self.pos.y = self.pos.y + disty
		
		# Preventing collision wall
		if self.pos.x <= 0 + self.collision_radius:
			if self.speed.x < self.max_speed:
				self.speed.x += self.turn_speed
                if self.pos.y <= 0 + self.collision_radius:
			if self.speed.y < self.max_speed:
				self.speed.y += self.turn_speed
                if self.pos.x >= screen.get_width() - self.collision_radius:
			if self.speed.x > -self.max_speed:
				self.speed.x -= self.turn_speed
                if self.pos.y > screen.get_height() - self.collision_radius:
			if self.speed.y > -self.max_speed:
                        	self.speed.y -= self.turn_speed
		
		# If  actual collision to the wall
		if self.pos.x <= 0 + self.radius:
                        self.speed.x = abs(self.speed.x)

                if self.pos.y <= 0 + self.radius:
                        self.speed.y = abs(self.speed.y)

                if self.pos.x >= screen.get_width() - self.radius:
                        self.speed.x = -abs(self.speed.x)

                if self.pos.y > screen.get_height() - self.radius:
                        self.speed.y = -abs(self.speed.y)
		
	# Draw tail
	def draw_vec_from_self(self):
        	tail = self.speed.normalized()
		pygame.draw.line(screen, self.color, (self.pos.x, self.pos.y), (self.pos.x - tail.x * self.tail_length, self.pos.y - tail.y * self.tail_length), self.tail_stroke)
	
	# Draw self
	def draw(self):
		self.draw_vec_from_self()
		pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
		
class Hoik(Boid):
	def __init__(self):
		Boid.__init__(self)
		
		# Movement
		self.speed = Vector2D(40,40)
		self.hunted_boid_heading = Vector2D(0,0)
		self.max_speed = 140
		
		# radius
		self.hunt_radius = 100
		
		# Graphics
		self.radius = 8
		self.color = (105, 0, 0)
		self.tail_length = 14
		self.tail_stroke = 2
		
		# Status
		self.ignore_flock = True
		
	def update_vectors(self, boids, hoiks, objects):
		self.avoid_collison_flock_member = Vector2D(0, 0)
		collision_members = 0
		for other_boid in hoiks:
			if self.pos != other_boid.pos:
				dp1p2 = self.pos - other_boid.pos
				# Check for collision other boids
				if self.collision_radius_other_boids + other_boid.radius >= dp1p2.magnitude():
					collision_members += 1
					self.avoid_collison_flock_member = self.avoid_collison_flock_member + other_boid.pos
		
		# Collision other hoik
		if collision_members != 0:
			# Preventing collision course with other flock members
			self.avoid_collison_flock_member.x = (self.avoid_collison_flock_member.x / collision_members)
			self.avoid_collison_flock_member.y = (self.avoid_collison_flock_member.y / collision_members)
			self.avoid_collison_flock_member.x = (self.pos.x - self.avoid_collison_flock_member.x)
			self.avoid_collison_flock_member.y = (self.pos.y - self.avoid_collison_flock_member.y)
				
		
		# Hunting Boid
		self.hunted_boid_heading = Vector2D(0, 0)
		flock_members = 0
		collision_members = 0
		for other_boid in boids:
			if self.pos != other_boid.pos:
				dp1p2 = self.pos - other_boid.pos

				# Check other boids to hunt
				if self.hunt_radius + other_boid.radius >= dp1p2.magnitude():
					collision_members += 1
					self.hunted_boid_heading = self.hunted_boid_heading + other_boid.pos
			
		# Hunting boid
		if collision_members != 0:
			# Calculating course for boids to hunt
			self.hunted_boid_heading.x = (self.hunted_boid_heading.x / collision_members)
			self.hunted_boid_heading.y = (self.hunted_boid_heading.y / collision_members)
			self.hunted_boid_heading.x = (self.hunted_boid_heading.x - self.pos.x)/4
			self.hunted_boid_heading.y = (self.hunted_boid_heading.y - self.pos.y)/4
		
			
		# Object collision
		self.avoid_collison_object = Vector2D(0, 0)
		for object in objects:
			
			# Preventing object collision
			dp1p2 = self.pos - object.pos
			if self.collision_radius_objects + object.radius >= dp1p2.magnitude():
				self.avoid_collison_object.x = object.pos.x
				self.avoid_collison_object.y = object.pos.y
				self.avoid_collison_object.x = (self.pos.x - self.avoid_collison_object.x)/2
				self.avoid_collison_object.y = (self.pos.y - self.avoid_collison_object.y)/2
				
				# Actual collision
				if self.radius + object.radius >= dp1p2.magnitude():
			 		self.speed = dp1p2
			
	def move(self, time_passed_seconds):
		# Calculate new speed vector
		self.speed = self.speed + self.hunted_boid_heading + self.avoid_collison_object + self.avoid_collison_flock_member
		
		# If Hoiks moves to slow speed them up
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) < self.min_speed:
			self.speed = self.speed * 1.3
			
		# If Hoiks moves to fast slow them down
		if ((abs(self.speed.x) + abs(self.speed.y)/2)) > self.max_speed:
			self.speed = self.speed * 0.9
			
		distx = time_passed_seconds * self.speed.x
		disty = time_passed_seconds * self.speed.y
		self.pos.x = self.pos.x + distx
		self.pos.y = self.pos.y + disty
		
		# Preventing collision wall
		if self.pos.x <= 0 + self.collision_radius:
			if self.speed.x < self.max_speed:
				self.speed.x += self.turn_speed
                if self.pos.y <= 0 + self.collision_radius:
			if self.speed.y < self.max_speed:
				self.speed.y += self.turn_speed
                if self.pos.x >= screen.get_width() - self.collision_radius:
			if self.speed.x > -self.max_speed:
				self.speed.x -= self.turn_speed
                if self.pos.y > screen.get_height() - self.collision_radius:
			if self.speed.y > -self.max_speed:
                        	self.speed.y -= self.turn_speed
		
		# If  actual collision to the wall
		if self.pos.x <= 0 + self.radius:
                        self.speed.x = abs(self.speed.x)

                if self.pos.y <= 0 + self.radius:
                        self.speed.y = abs(self.speed.y)

                if self.pos.x >= screen.get_width() - self.radius:
                        self.speed.x = -abs(self.speed.x)

                if self.pos.y > screen.get_height() - self.radius:
                        self.speed.y = -abs(self.speed.y)

# Implementasion of circle objects
class circle_object(Vector2D):
	def __init__(self, x, y, radius, color):
		Vector2D.__init__(self, 0, 0)
		self.pos = Vector2D(x, y)
		self.radius = radius
		self.color = color
		
	def draw(self):
		pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)

# How many boids to simulate
boids = []
for x in range(random.randrange(5, 10)):		
	boids.append(Boid())

# How many hoiks to simulate
hoiks = []
for y in range(0):		
	hoiks.append(Hoik())

# Game objects
objects = [] 
#[circle_object(30, 100, 20, (0, 0, 0))]
	
clock = pygame.time.Clock()

SCREEN_COLOR = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))

while True:
        for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == QUIT or key[pygame.K_ESCAPE]:
                        exit()
	pygame.draw.rect(screen, (SCREEN_COLOR), (0, 0, screen.get_width(), screen.get_height()))
        time_passed = clock.tick(30) # limit to x FPS 
        time_passed_seconds = time_passed / 1000.0

	# Update boids
	for boid in boids:
		boid.update_vectors(boids, hoiks, objects)
		boid.move(time_passed_seconds)
		boid.draw()
	
	# Update Hoiks
#	for hoik in hoiks:
#		hoik.update_vectors(boids, hoiks, objects)
#		hoik.move(time_passed_seconds)
#		hoik.draw()
	
	# Draw Objects
#	for obj in objects:
#		obj.draw()
		
	pygame.display.update()
	
