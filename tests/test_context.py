from ..gssceneloader.context import Context


class TestContext:
    def test_construct(self):
        context = Context()
        assert context.seed == 0
        assert context.generator.initial_seed() == 0
