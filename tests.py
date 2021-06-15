from Behaviors import Behaviors

israel_behaviors = Behaviors()
gilad_behaviors = Behaviors()
dict = {}
dict["israel"] = [israel_behaviors, False]
if "israel" in dict:
    print("israel in dict")
if "gilad" not in dict:
    dict["gilad"] = [gilad_behaviors, True]

dict["gilad"][0].happy += 1
print(gilad_behaviors.happy)
dict["israel"][0].happy += 1
print(israel_behaviors.happy)
print(gilad_behaviors.total)
print(israel_behaviors.total)

for participant in dict:
    dict[participant][0].update_total()

print(gilad_behaviors.total)
print(israel_behaviors.total)