$(document).ready(function() {

  var Article = Backbone.Model.extend({
    urlRoot: '/api/articles'
  });

  var Articles = Backbone.Collection.extend({
    model: Article,
    url: '/api/articles'
  });

  var DisplayArticle = Backbone.View.extend({
    el: "#article",
    template: _.template($("#display-article").html()),
    events: {
      'click .display-articles': 'displayArticles'
    },
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.model.on('request', this.showSpinner, this);
      this.model.on('sync', this.render, this);
      this.model.fetch();
    },
    render: function() {
      this.hideSpinner().done(_.bind(function() {
        this.$el.html(this.template(this.model.attributes));
      }, this));
    },
    displayArticles: function(e) {
      e.preventDefault();
      this.event_agg.trigger("displayArticles");
    },
    showSpinner: function() {
      return $(".fa-spin").fadeIn().promise();
    },
    hideSpinner: function() {
      return $(".fa-spin").fadeOut().promise();
    }
  });

  var ArticlePreview = Backbone.View.extend({
    tagName: 'li',
    className: 'article-preview col-xs-12',
    template: _.template($("#article-preview").html()),
    events: {
      'click img': 'displayArticle',
      'click .image-text': 'displayArticle',
      'click .read-more': 'displayArticle'
    },
    initialize: function(options) {
      this.event_agg = options.event_agg;
    },
    render: function() {
      this.$el.html(this.template(this.model.attributes));
      return this;
    },
    displayArticle: function(e) {
      e.preventDefault();
      this.event_agg.trigger("displayArticle", this.model.get('slug'));
    }
  });

  var ArticlesGrid = Backbone.View.extend({
    el: '#articles-grid',
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.collection.on('add', this.showSpinner, this);
      this.collection.on('sync', this.render, this);
    },
    render: function() {
      this.hideSpinner().done(_.bind(function() {
        this.$el.remove("li");
        this.collection.each(this.addArticle, this);
        return this;
      }, this));
    },
    addArticle: function(article) {
      var articlePreview = new ArticlePreview({
        model: article,
        event_agg: this.event_agg
      });
      this.$el.append(articlePreview.render().el);
    },
    showSpinner: function() {
      return $(".fa-spin").fadeIn().promise();
    },
    hideSpinner: function() {
      return $('.fa-spin').fadeOut().promise();
    }
  });

  var Container = Backbone.View.extend({
    el: '#feed-container',
    template: _.template($("#spa-container").html()),
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.event_agg.bind("displayArticle", this.displayArticle, this);
      this.event_agg.bind("displayArticles", this.displayArticles, this);
      this.render(options.slug);
    },
    render: function(slug) {
      this.$el.html(this.template());
      // decide which child view we should render based on slug
      if (slug) {
        this.displayArticle(slug);
      }
      else { this.displayArticles(); }
    },
    displayArticle: function(slug) {
      this.$("#articles-grid").empty();
      this.goTo('/' + slug);
      var displayedArticle = new DisplayArticle({
        model: new Article({id: slug}),
        event_agg: this.event_agg
      });
    },
    displayArticles: function() {
      this.$(".article").empty();
      this.goTo('/');
      var articles = new Articles();
      articles.fetch();
      this.articleGrid = new ArticlesGrid({
        collection: articles,
        event_agg: this.event_agg
      });
    },
  });

  var Router = Backbone.Router.extend({
    routes: {
      "": "displayArticles",
      ":slug" : "displayArticle",
    },
    displayArticles: function() {
      this.initContainer(null);
    },
    displayArticle: function(slug) {
      this.initContainer(slug);
    },
    initContainer: function(slug) {
      var container = new Container({
        event_agg: _.extend({}, Backbone.Events),
        slug: slug
      });
    }
  });

  var router = new Router();

  Backbone.View.prototype.goTo = function (uri) {
    router.navigate(uri);
  };

  Backbone.history.start({
    pushState: true,
    root: "/feed/"
  });

});