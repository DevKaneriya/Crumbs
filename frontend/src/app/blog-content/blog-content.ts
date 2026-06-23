import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-blog-content',
  standalone: true,
  imports: [Header, Footer, CommonModule],
  templateUrl: './blog-content.html',
  styleUrl: './blog-content.css'
})
export class BlogContent {

  blogs = [

    {
      img: "assets/blogs/blog1.png",
      title: "The Story Behind the Word Mukhwas",
      route: "story-behind-the-word-mukhwas",
      parts: [
        {
          subHeader: '',
          content: [
            `When you think of Indian hospitality, one of the most delightful traditions 
          that comes to mind is the small bowl of colorful seeds and sweet mixes served after a hearty meal. 
          This humble treat is known as Mukhwas, a name that has been cherished in households, restaurants, 
          and festive gatherings across India.`,

            `But have you ever wondered where the word Mukhwas comes from and what it truly means? 
          Let’s explore the story behind it.`
          ]
        },
        {
          subHeader: '📖 Breaking Down the Word: Mukh + Was',
          content: [
            'The word Mukhwas is derived from two simple Hindi/Sanskrit-origin words:',
            {
              list: [
                'Mukh (मुख) – meaning mouth',
                'Vas (वास) – meaning smell, fragrance, or aroma'
              ]
            },
            `Put together, Mukhwas literally translates to “fragrance for the mouth” or “mouth freshener.” 
          This perfectly describes its role – a refreshing mixture that not only aids digestion but also leaves a pleasant aroma.`
          ]
        },
        {
          subHeader: '🌸 A Tradition Rooted in Culture',
          content: [
            'In ancient India, eating was never just about filling the stomach; it was a ritual that combined nourishment, digestion, and satisfaction.',
            {
              list: [
                'After meals, people were often offered fennel seeds (saunf), cardamom, or cloves to cleanse the palate.',
                'Over time, these evolved into flavored mixes with herbs, spices, seeds, sugar crystals, and even rose petals.',
                'This aromatic blend became known as Mukhwas, symbolizing both fresh breath and good hospitality.'
              ]
            },
            'In many Indian households today, offering Mukhwas after meals is considered a gesture of warmth and care for guests.'
          ]
        },
        {
          subHeader: '🌿 More Than Just Fresh Breath',
          content: [
            'While the name emphasizes freshness, Mukhwas is much more than a mouth freshener:',
            {
              list: [
                '<b>Digestive Aid:</b> Ingredients like fennel, ajwain, and sesame help improve digestion.',
                '<b>Cooling Effect:</b> Certain mixes use aniseed and menthol for a soothing aftertaste.',
                '<b>Festive Symbol:</b> Special versions with silver-coated seeds, saffron, or rose petals are served during weddings and festivals.'
              ]
            },
            'So, when we say “Mukhwas,” it isn’t just about freshening the mouth – it’s about ending a meal on a fragrant, flavorful, and healthy note.'
          ]
        },
        {
          subHeader: '✨ The Modern-Day Mukhwas',
          content: [
            'Today, the word Mukhwas is not just limited to tradition. Modern variations include:',
            {
              list: [
                'Sugar-free mukhwas for health-conscious consumers',
                'Chocolate and mint mukhwas for a fusion twist',
                'Luxury mukhwas jars for gifting in weddings, festivals, and corporate events'
              ]
            },
            'Despite the innovations, the essence of the word remains unchanged: Mukhwas is, and will always be, the fragrance for your mouth.'
          ]
        },
        {
          subHeader: '🌺 Final Thoughts',
          content: [
            `The story behind the word Mukhwas is a reminder that sometimes the simplest words carry the richest cultural heritage. 
          It’s more than just an after-meal ritual—it’s a tradition that connects families, celebrates hospitality, and preserves the essence of Indian food culture.`,

            `So the next time you enjoy a spoonful of Mukhwas, remember—you’re not just freshening your mouth, 
          you’re carrying forward a centuries-old tradition wrapped in flavor and fragrance. 🌿`
          ]
        }
      ]
    },
    {
      img: "assets/blogs/blog2.jpg",
      title: "Health Benefits of Mukhwas Ingredients",
      route: "health-benefits-of-mukhwas-ingredients",
      parts: [
        {
          subHeader: '',
          content: [
            `If you’ve ever been served a small bowl of colorful seeds after a meal in India, 
      you’ve enjoyed Mukhwas — a traditional mouth freshener with a rich heritage. 
      But Mukhwas is more than just a way to refresh your breath. 
      Behind those vibrant fennel seeds, sesame crunchies, rose petals, and tiny sugar-coated delights 
      lies a world of health benefits.`,

            `Let’s uncover the amazing health benefits of Mukhwas ingredients and why this age-old tradition is worth keeping alive.`
          ]
        },
        {
          subHeader: '🍃 1. Fennel Seeds (Saunf)',
          content: [
            {
              list: [
                '<b>Digestive Powerhouse:</b> Fennel seeds are widely known for easing digestion and reducing bloating.',
                '<b>Fresh Breath:</b> Their natural oils act as a breath freshener.',
                '<b>Rich in Antioxidants:</b> They help detoxify the body and support overall wellness.'
              ]
            },
            '👉 That’s why restaurants often serve fennel after meals — it’s a natural digestive aid!'
          ]
        },
        {
          subHeader: '🌱 2. Sesame Seeds (Til)',
          content: [
            {
              list: [
                '<b>Rich in Nutrients:</b> Packed with calcium, iron, and magnesium, sesame seeds are great for bone and heart health.',
                '<b>Good Fats:</b> They contain healthy fats that boost energy and improve skin health.',
                '<b>Hormonal Balance:</b> Especially beneficial for women, sesame seeds help regulate hormones naturally.'
              ]
            }
          ]
        },
        {
          subHeader: '🌸 3. Rose Petals (Gulkand or Dry Rose)',
          content: [
            {
              list: [
                '<b>Cooling Effect:</b> Rose petals soothe the stomach and reduce acidity.',
                '<b>Mood Enhancer:</b> Gulkand (sweetened rose petal preserve) is known in Ayurveda as a natural stress reliever.',
                '<b>Rich in Antioxidants:</b> Helps improve skin health and boosts immunity.'
              ]
            }
          ]
        },
        {
          subHeader: '🌿 4. Ajwain (Carom Seeds)',
          content: [
            {
              list: [
                '<b>Digestive Aid:</b> Carom seeds help relieve indigestion, acidity, and stomach discomfort.',
                '<b>Anti-Inflammatory:</b> Their natural compounds soothe internal inflammation.',
                '<b>Boosts Metabolism:</b> Ajwain is also linked to better fat metabolism.'
              ]
            }
          ]
        },
        {
          subHeader: '🌰 5. Cardamom (Elaichi)',
          content: [
            {
              list: [
                '<b>Freshens Breath Naturally:</b> Known as the “queen of spices,” cardamom leaves a sweet aroma in the mouth.',
                '<b>Detoxifying Agent:</b> Helps in flushing out toxins from the body.',
                '<b>Supports Heart Health:</b> Contains compounds that may reduce blood pressure and cholesterol.'
              ]
            }
          ]
        },
        {
          subHeader: '🍂 6. Cloves (Laung)',
          content: [
            {
              list: [
                '<b>Anti-Inflammatory:</b> Cloves contain eugenol, a powerful compound for pain relief and reducing inflammation.',
                '<b>Boosts Immunity:</b> Known for their antibacterial and antiviral properties.',
                '<b>Oral Health:</b> Traditionally used to strengthen gums and reduce bad breath.'
              ]
            }
          ]
        },
        {
          subHeader: '🥥 7. Coconut Flakes (often added in some Mukhwas blends)',
          content: [
            {
              list: [
                '<b>Good Fats & Fiber:</b> Keeps you full and supports digestion.',
                '<b>Energy Booster:</b> Provides instant natural energy.',
                '<b>Supports Immunity:</b> Contains lauric acid with antimicrobial benefits.'
              ]
            }
          ]
        },
        {
          subHeader: '✨ The Balanced Blend of Benefits',
          content: [
            'Mukhwas is not just a mouth freshener — it’s a digestive, detoxifier, and wellness booster rolled into one. By combining seeds, spices, and herbs, this traditional mix delivers:',
            {
              list: [
                '✅ Improved Digestion',
                '✅ Fresh Breath',
                '✅ Rich Source of Nutrients',
                '✅ Stress Relief & Relaxation',
                '✅ Support for Gut Health'
              ]
            }
          ]
        },
        {
          subHeader: '🌺 Final Thoughts',
          content: [
            `The next time you take a spoonful of Mukhwas, remember you’re not just enjoying a flavorful after-meal treat — 
      you’re also giving your body a gentle boost of health. From fennel’s digestive magic to rose’s calming effect, 
      every ingredient adds its own unique benefit.`,

            `So, go ahead — savor the taste, embrace the tradition, and enjoy the health benefits of Mukhwas ingredients every day. 🌿`
          ]
        }
      ]
    },
    {
      img: "assets/blogs/blog3.png",
      title: "Why Restaurants Always Serve Fennel Seeds After Meals",
      route: "why-restaurants-serve-fennel-seeds-after-meals",
      parts: [
        {
          subHeader: '',
          content: [
            `If you’ve dined at an Indian restaurant, you’ve probably noticed a small bowl of fennel seeds (saunf) served at the end of your meal. 
      Sometimes they’re plain, sometimes sugar-coated, and often mixed with colorful mukhwas. 
      But have you ever wondered why fennel seeds are such a common after-meal tradition?`,

            `The answer goes beyond taste — fennel seeds bring together culture, health, and hospitality in every spoonful.`
          ]
        },
        {
          subHeader: '🍃 1. Natural Digestive Aid',
          content: [
            'One of the main reasons fennel seeds are served after meals is their powerful effect on digestion. Fennel contains essential oils that:',
            {
              list: [
                'Stimulate the secretion of digestive enzymes',
                'Reduce bloating and gas',
                'Ease stomach cramps'
              ]
            },
            'This makes fennel the perfect way to end a heavy meal.'
          ]
        },
        {
          subHeader: '🌸 2. Instant Mouth Freshener',
          content: [
            `Fennel seeds have a naturally sweet, refreshing flavor. 
      Chewing them releases aromatic oils that leave your mouth feeling fresh and clean — 
      a simple, natural alternative to chewing gum or artificial mints.`,

            `Restaurants serve them to ensure guests leave with a pleasant aftertaste.`
          ]
        },
        {
          subHeader: '🌿 3. Cooling Effect on the Body',
          content: [
            `In Ayurveda, fennel is known for its cooling properties. 
      After spicy or oily food, chewing fennel helps balance the heat in the stomach and soothes acidity. 
      That’s why they’re a popular choice in Indian cuisine, where spices are abundant.`
          ]
        },
        {
          subHeader: '🍬 4. Sweet Ending Without Dessert',
          content: [
            `Many restaurants mix fennel with sugar-coated versions or colorful mukhwas blends. 
      This adds a touch of sweetness at the end of the meal, almost like a light dessert, without being heavy.`
          ]
        },
        {
          subHeader: '🧡 5. A Gesture of Hospitality',
          content: [
            'Beyond health, serving fennel seeds has become a symbol of care and tradition. Just as tea might be offered in other cultures, Indian restaurants use fennel as a way to:',
            {
              list: [
                'Honor tradition',
                'Show thoughtfulness toward guests',
                'Leave diners with a memorable final impression'
              ]
            }
          ]
        },
        {
          subHeader: '✨ The Science Behind the Tradition',
          content: [
            `Modern research supports what tradition has known for centuries: fennel seeds contain compounds like anethole that relax stomach muscles and aid digestion. 
      They’re also rich in antioxidants, fiber, and essential nutrients — making them a small but mighty superfood.`
          ]
        },
        {
          subHeader: '🌺 Final Thoughts',
          content: [
            `The next time you’re offered a bowl of fennel seeds at a restaurant, remember — it’s not just about freshening your breath. 
      It’s about better digestion, cooling your body, and a touch of cultural tradition passed down through generations.`,

            `So, chew a spoonful, enjoy the flavor, and appreciate the thoughtful gesture — 
      because sometimes, the smallest rituals carry the biggest meaning. 🌿`
          ]
        }
      ]
    }

  ]
  currentBlog: any | null;
  filterredBlog: any;


  constructor(private activeRoute: ActivatedRoute,
    private router: Router) { }

  navigate(slug: string) {
    this.router.navigate(['/blogs', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  ngOnInit(): void {
    this.activeRoute.paramMap.subscribe(params => {
      this.currentBlog = params.get('route');
      this.filterredBlog = this.blogs.find(blog => blog.route === this.currentBlog);
    }
    );

  }

}
