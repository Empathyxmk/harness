import pytest

from src.graphql_query_builder.index import Query

def remove_spaces(s):
    return str(s).replace(' ', '').replace('\t', '').replace('\n', '')

def test_should_accept_single_find_value():
    expeted = "user{age}"
    user = Query("user").find("age")
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_create_query_with_function_name_and_alia():
    expeted = "sam : user{name}"
    user = Query("user", "sam").find("name")
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_create_query_with_function_name_and_input():
    expeted = "user(id:12345){name}"
    user = Query("user", {"id": 12345}).find("name")
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_create_query_with_function_name_and_inputs():
    expeted = "user(id:12345, age:34){name}"
    user = Query("user", {"id": 12345, "age": 34}).find("name")
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_accept_single_find_value_with_alia():
    expeted = "user{nickname:name}"
    user = Query("user").find({"nickname": "name"})
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_accept_multiple_find_values():
    expeted = "user{firstname, lastname}"
    user = Query("user").find("firstname", "lastname")
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_accept_array_find_values():
    expeted = "user{firstname, lastname}"
    user = Query("user").find(["firstname", "lastname"])
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_work_with_nesting_queries():
    expeted = (
        "user( id:12345 ) {"
        "id,	nickname : name,	isViewerFriend,"
        "image : profilePicture( size:50 ) {"
        "uri,	width,		height	}	  }"
    )

    profilePicture = Query("profilePicture", {"size": 50})
    profilePicture.find("uri", "width", "height")

    user = Query("user", {"id": 12345})
    user.find(["id", {"nickname": "name"}, "isViewerFriend", {"image": profilePicture}])

    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_work_with_simple_nesting_queries():
    expeted = "user { profilePicture { uri, width, height } }"
    user = Query("user")
    user.find({"profilePicture": ["uri", "width", "height"]})
    assert remove_spaces(expeted) == remove_spaces(user)

def test_should_be_able_to_group_queries():
    expeted = (
        'FetchLeeAndSam { lee: user(id: "1") { name	},'
        'sam: user(id: "2") { name	}  }'
    )

    FetchLeeAndSam = Query("FetchLeeAndSam")

    lee = Query("user", {"id": "1"})
    lee.setAlias("lee")
    lee.find(["name"])

    sam = Query("user", "sam")
    sam.filter({"id": "2"})
    sam.find("name")

    FetchLeeAndSam.find(lee, sam)
    assert remove_spaces(expeted) == remove_spaces(FetchLeeAndSam)

def test_should_work_with_nasted_objects_and_lists():
    expeted = (
        'myPost:Message(type:"chat",message:"yoyo",'
        'user:{name:"bob",screen:{height:1080,width:1920}},'
        'friends:[{id:1,name:"ann"},{id:2,name:"tom"}])  {'
        'messageId : id, postedTime : createTime }'
    )
    MessageRequest = {
        "type": "chat",
        "message": "yoyo",
        "user": {
            "name": "bob",
            "screen": {"height": 1080, "width": 1920}
        },
        "friends": [{"id": 1, "name": "ann"}, {"id": 2, "name": "tom"}]
    }
    MessageQuery = Query("Message", "myPost")
    MessageQuery.filter(MessageRequest)
    MessageQuery.find({"messageId": "id"}, {"postedTime": "createTime"})
    assert remove_spaces(expeted) == remove_spaces(MessageQuery)

def test_should_work_with_objects_that_have_help_functions():
    expeted = 'inventory(toy:"jack in the box")  { id }'
    class ChildsToyType(dict):
        def getState(self):
            pass
    ChildsToy = ChildsToyType({"toy": "jack in the box"})
    ChildsToy.getState()
    ItemQuery = Query("inventory", ChildsToy)
    ItemQuery.find("id")
    assert remove_spaces(expeted) == remove_spaces(ItemQuery)

def test_should_work_with_nasted_objects_that_have_help_functions():
    expeted = 'inventory(toy:"jack in the box")  { id }'
    class Utils(dict):
        def getState(self):
            pass
    class ChildsToyType(dict):
        pass
    ChildsToy = ChildsToyType({"toy": "jack in the box", "utils": Utils()})
    ChildsToy["utils"].getState()
    ItemQuery = Query("inventory", ChildsToy)
    ItemQuery.find("id")
    assert remove_spaces(expeted) == remove_spaces(ItemQuery)

def test_should_skip_empty_objects_in_filter_args():
    expeted = 'inventory(toy:"jack in the box")  { id }'
    ChildsToy = {"toy": "jack in the box", "utils": {}}
    ItemQuery = Query("inventory", ChildsToy)
    ItemQuery.find("id")
    assert remove_spaces(expeted) == remove_spaces(ItemQuery)

def test_should_throw_if_find_input_items_have_zero_props():
    with pytest.raises(Exception):
        Query("x").find({})

def test_should_throw_if_find_input_items_have_multiple_props():
    with pytest.raises(Exception):
        Query("x").find({"a": "z", "b": "y"})

def test_should_throw_if_find_is_undefined():
    with pytest.raises(Exception):
        Query("x").find()

def test_should_throw_if_no_find_values_have_been_set():
    with pytest.raises(Exception):
        str(Query("x"))

def test_should_throw_if_find_is_not_valid():
    with pytest.raises(Exception):
        Query("x").find(123)

def test_should_throw_if_accidentally_pass_undefined():
    with pytest.raises(Exception):
        Query("x", None)

def test_should_throw_if_not_an_input_object_for_alias():
    with pytest.raises(Exception):
        Query("x", True)