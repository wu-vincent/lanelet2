#include "lanelet2_traffic_rules/TrafficRulesFactory.h"

#include "lanelet2_traffic_rules/GermanTrafficRules.h"

namespace lanelet {

#if __cplusplus < 201703L
constexpr char Locations::Germany[];
#endif

namespace traffic_rules {
namespace {
RegisterTrafficRules<GermanVehicle> gvRules(Locations::Germany, Participants::Vehicle);
RegisterTrafficRules<GermanPedestrian> gpRules(Locations::Germany, Participants::Pedestrian);
RegisterTrafficRules<GermanBicycle> gbRules(Locations::Germany, Participants::Bicycle);
}  // namespace

TrafficRulesUPtr TrafficRulesFactory::create(const std::string& location, const std::string& participant,
                                             TrafficRules::Configuration configuration) {
  auto& registry = instance().registry_;
  auto elem = registry.find(std::make_pair(location, participant));
  const std::string vehicle = Participants::Vehicle;
  if (elem == registry.end() && participant.compare(0, vehicle.size(), vehicle) == 0) {
    // second try for vehicle types
    elem = registry.find(std::make_pair(location, std::string(Participants::Vehicle)));
  }
  if (elem != registry.end()) {
    configuration["location"] = location;
    configuration["participant"] = participant;
    return elem->second(configuration);
  }
  throw InvalidInputError("No matching traffic rules found for location " + location + ", participant " + participant);
}

std::vector<std::pair<std::string, std::string>> TrafficRulesFactory::availableTrafficRules() {
  std::vector<std::string> rules;
  auto& registry = TrafficRulesFactory::instance().registry_;
  return utils::transform(registry, [](const auto& elem) { return elem.first; });
}

TrafficRulesFactory& TrafficRulesFactory::instance() {
  static TrafficRulesFactory factory;
  return factory;
}
}  // namespace traffic_rules
}  // namespace lanelet
