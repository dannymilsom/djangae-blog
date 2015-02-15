$(document).ready(function() {

  var Article = Backbone.Model.extend();

  var Articles = Backbone.Collection.extend({
    model: Article,
    url: '/api/articles'
  });

  var DisplayArticle = Backbone.View.extend({
    template: _.template($("#display-article").html()),
    id: 'article',
    className: 'article col-xs-12 col-sm-8',
    events: {
      'click .display-articles': 'displayArticles'
    },
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.render();
    },
    render: function() {
      this.$el.html(this.template(this.model.attributes));
      return this;
    },
    displayArticles: function(e) {
      e.preventDefault();
      this.event_agg.trigger("displayArticles");
    }
  });

  var ArticlePreview = Backbone.View.extend({
    tagName: 'li',
    className: 'article-preview col-xs-12',
    template: _.template($("#article-preview").html()),
    events: {
      'click img': 'displayArticle',
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
      this.event_agg.trigger("displayArticle", this.model);
    }
  });

  var ArticlesGrid = Backbone.View.extend({
    el: '#articles-grid',
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.collection.on('sync', this.render, this);
    },
    render: function() {
      this.$el.empty();
      this.collection.each(this.addArticle, this);
      return this;
    },
    addArticle: function(article) {
      var articlePreview = new ArticlePreview({
        model: article,
        event_agg: this.event_agg
      });
      this.$el.append(articlePreview.render().el);
    }
  });

  var Container = Backbone.View.extend({
    el: '#container',
    template: _.template($("#spa-container").html()),
    initialize: function(options) {
      this.event_agg = options.event_agg;
      this.event_agg.bind("displayArticle", this.displayArticle, this);
      this.event_agg.bind("displayArticles", this.displayArticles, this);
      this.render();
      this.displayArticles();
    },
    render: function() {
      this.$el.html(this.template());
    },
    displayArticle: function(article) {
      this.$("#articles-grid").empty();
      var displayedArticle = new DisplayArticle({
        model: article,
        event_agg: this.event_agg
      });
      this.$el.append(displayedArticle.render().el);
    },
    displayArticles: function() {
      this.$(".article").remove();
      var articles = new Articles();
      articles.fetch();
      this.articleGrid = new ArticlesGrid({
        collection: articles,
        event_agg: this.event_agg
      });
    },
  });

  var vent = _.extend({}, Backbone.Events);

  var container = new Container({
    event_agg: vent
  });

});