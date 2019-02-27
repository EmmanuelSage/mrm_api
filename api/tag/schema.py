import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from api.tag.models import Tag as TagModel
from utilities.validations import validate_empty_fields
from utilities.utility import update_entity_fields
from helpers.auth.authentication import Auth
from helpers.auth.error_handler import SaveContextManager


class Tag(SQLAlchemyObjectType):
    """
        Autogenerated return type of a tag
    """
    class Meta:
        model = TagModel


class CreateTag(graphene.Mutation):
    """
        Returns payload of creating a tag
    """
    class Arguments:
        name = graphene.String(required=True)
        color = graphene.String(required=True)
        description = graphene.String(required=True)
    tag = graphene.Field(Tag)

    @Auth.user_roles('Admin')
    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        tag = TagModel(**kwargs)
        payload = {
            'model': TagModel, 'field': 'name', 'value':  kwargs['name']
            }
        with SaveContextManager(
           tag, 'Tag', payload
        ):
            return CreateTag(tag=tag)


class UpdateTag(graphene.Mutation):
    """
        Returns payload of updating a tag
    """
    class Arguments:
        tag_id = graphene.Int(required=True)
        name = graphene.String()
        color = graphene.String()
        description = graphene.String()
    tag = graphene.Field(Tag)

    @Auth.user_roles('Admin')
    def mutate(self, info, tag_id, **kwargs):
        validate_empty_fields(**kwargs)
        query_tag = Tag.get_query(info)
        tag = query_tag.filter(
            TagModel.id == tag_id).first()
        if not tag:
            raise GraphQLError("Tag not found")
        update_entity_fields(tag, **kwargs)
        tag.save()
        return UpdateTag(tag=tag)


class DeleteTag(graphene.Mutation):
    """
    Returns payload on deleting a tag
    """
    class Arguments:
        tag_id = graphene.Int(required=True)
        state = graphene.String()
    tag = graphene.Field(Tag)

    @Auth.user_roles('Admin')
    def mutate(self, info, tag_id, **kwargs):
        query = Tag.get_query(info)
        result = query.filter(TagModel.state == "active")
        tag = result.filter(
            TagModel.id == tag_id).first()
        if not tag:
            raise GraphQLError("Tag not found")
        update_entity_fields(tag, state="archived", **kwargs)
        tag.save()
        return DeleteTag(tag=tag)


class Mutation(graphene.ObjectType):
    create_tag = CreateTag.Field(
        description="Creates a new tag with the arguments\
            \n- name: The name field of the tag[required]\
            \n- color: The color field of the tag[required]\
            \n- description: The description the tag")
    update_tag = UpdateTag.Field(
        description="Updates a tag with the arguments\
            \n- tag_id: Unique identifier of the tag[required]\
            \n- name: The name field of the tag\
            \n- color: The color field of the tag\
            \n- description: The description the tag")
    delete_tag = DeleteTag.Field(
        description="Deletes a tag having arguments\
            \n- tag_id: Unique identifier of the tag[required]\
            \n- state: Check if the tag is active, archived or deleted")
