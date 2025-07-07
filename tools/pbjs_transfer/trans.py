# -*- coding: utf-8 -*-
import json
import example_pb2

# 使用编译器生成python代码：protoc --python_out=. example.proto

# 将PB对象转换为JSON字符串
def pb_to_json(pb_obj):
    """Convert a Protocol Buffer object to a JSON string."""
    pb_dict = {}
    for field_descriptor in pb_obj.DESCRIPTOR.fields:
        field_value = getattr(pb_obj, field_descriptor.name)
        pb_dict[field_descriptor.name] = field_value
    return json.dumps(pb_dict, indent=2)

# 将JSON字符串转换为PB对象
def json_to_pb(json_data):
    """Convert a JSON string to a Protocol Buffer object."""
    pb_obj = example_pb2.Person()
    json_dict = json.loads(json_data)
    for field_name, field_value in json_dict.items():
        setattr(pb_obj, field_name, field_value)
    return pb_obj

# 示例使用
def create_pb_person(name="alice",age=18,email="alice@example.com"):
    # 创建一个PB对象
    person = example_pb2.Person()
    person.name = name
    person.age = age
    person.email = email
    return person


if __name__ == "__main__":
    p = create_pb_person()
    # 将PB对象转换为JSON字符串
    json_str = pb_to_json(p)
    print("PB to JSON:")
    print(json_str)

    # 将JSON字符串转换为PB对象
    new_person = json_to_pb(json_str)
    print("\nJSON to PB:")
    print(f"Name: {new_person.name}")
    print(f"Age: {new_person.age}")
    print(f"Email: {new_person.email}")