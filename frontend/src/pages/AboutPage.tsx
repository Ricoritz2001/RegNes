
const meanItems = [
  {
    title: 'Sentiments Mean',
    text: `Average sentiment of all regional news items using the Sentiment Wortschatz
           and German Polarity Clues by Remus et al. (2010) and Waltinger (2010),
           correcting for negations as suggested by Rauh (2018).`,
  },
  {
    title: 'Happiness Mean',
    text: `Average happiness value of all regional news items using Dodds et al. (2011)’s
           German Hedometer happiness scores.`,
  },
  {
    title: 'Valenz Mean',
    text: `Average valence score of all regional news items using the affect value
           dataset by Köper & Im Walde (2018).`,
  },
];

export default function AboutPage() {
  return (
    <section className="min-h-screen bg-gradient-to-r from-cyan-700 via-cyan-500 to-blue-400 flex items-center">
      <div className="container mx-auto px-4 py-16 space-y-12">
        {/* Page Title */}
        <h1 className="text-4xl font-bold text-white text-center">
          About This Dashboard
        </h1>

        {/* General Information */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            General Information
          </h2>
          <p className="text-gray-700">
            The RegNeS (Regional News Syndication) database is a daily collection of
            German-language media headlines started in July 2019. Its heart is a
            twice-daily download of headlines and article snippets from print and online
            media outlets (current numbers below). Notably, newspapers and radio stations
            (sources) may have multiple channels. The set of media sources includes
            regional and national outlets from the German-speaking world (Germany,
            Austria, Liechtenstein, Luxembourg, Switzerland). In the dashboard,
            only regional news are considered—national and international news sources
            are not presented. Geolocation of news articles is based on the news
            channels’ locations (e.g., editorial desks) and the regions they target.
          </p>
        </div>

       
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {meanItems.map(({ title, text }) => (
            <div
              key={title}
              className="bg-white p-6 rounded-lg shadow-md flex flex-col"
            >
              <h3 className="text-xl font-semibold mb-3 text-gray-800">
                {title}
              </h3>
              <p className="text-gray-700 flex-1">{text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
