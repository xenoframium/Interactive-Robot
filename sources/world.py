from projectile import *
from targets import *

class World:
    def __init__(self):
        self.projectiles = []
        self.shootable_targets = []
        self.treadable_targets = []
        self.additions = []
        self.removals = []

    def update_projectiles(self):
        for obj in self.additions:
            self.projectiles.append(obj)

        self.additions = []

        for obj in self.removals:
            obj.destroy()
            try:
                self.projectiles.remove(obj)
            except ValueError:
                pass

        self.removals = []

        for obj in self.projectiles:
            obj.update()
            if obj.should_despawn():
                self.removals.append(obj)

    def update_target_collisions(self, robot):
        for projectile in self.projectiles:
            for target in self.shootable_targets:
                if (projectile.position - target.position).magnitude() < PROJECTILE_SIZE / 2 + TARGET_SIZE / 2:
                    self.remove_projectile(projectile)
                    target.destroy()
                    self.shootable_targets.remove(target)

        for target in self.treadable_targets:
            if (robot.position - target.position).magnitude() < ROBOT_BODY_SIZE / 2 + TARGET_SIZE / 2:
                target.destroy()
                self.treadable_targets.remove(target)

    def update(self, robot):
        self.update_projectiles()
        self.update_target_collisions(robot)

    def add_projectile(self, projectile):
        self.additions.append(projectile)

    def remove_projectile(self, projectile):
        self.removals.append(projectile)